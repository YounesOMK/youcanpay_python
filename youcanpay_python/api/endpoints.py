from abc import ABC, abstractmethod
from typing import Optional


from youcanpay_python.api.service import APIService
from youcanpay_python.exceptions.exceptions import (
    MissingTokenException,
    ServerException,
    UnexpectedResultException,
    UnsetPrivateKeyException,
    UnsetPublicKeyException,
    UnsupportedResponseException,
    ValidationException,
)
from youcanpay_python.models.data import Response
from youcanpay_python.models.token import Token, TokenData


class BaseEndpoint(ABC):
    def __init__(self, api_service: APIService) -> None:
        self.api_service = api_service

    @abstractmethod
    def endpoint(self) -> str:
        pass

    def list_endpoint(self) -> str:
        return self.endpoint()

    def single_endpoint(self, id: str) -> str:
        return f"{self.endpoint()}/{id}"

    def create_endpoint(self) -> str:
        return self.endpoint()

    def assert_private_key_is_set(self):
        if self.api_service.private_key is None:
            raise UnsetPrivateKeyException("private key not set")

    def assert_public_key_is_set(self):
        if self.api_service.public_key is None:
            raise UnsetPublicKeyException("public key not set")


class KeysEndpoint(BaseEndpoint):
    BASE_ENDPOINT = "keys"

    def endpoint(self):
        return self.BASE_ENDPOINT

    def check(
        self, private_key: Optional[str] = None, public_key: Optional[str] = None
    ):
        if private_key is None and public_key is None:
            return False

        response = self.api_service.post(
            f"{self.BASE_ENDPOINT}/check",
            json={"pri_key": private_key, "pub_key": public_key},
        )

        return self.assert_response(response)

    def assert_response(self, response: Response):
        if response.status_code == 200:
            return True

        if 500 <= response.status_code < 600:
            raise ServerException(
                "Internal error from server. Support has been notified. Please try again!",
                str(response.data),
                response.status_code,
            )


class TokenEndpoint(BaseEndpoint):
    BASE_ENDPOINT = "tokenize"

    def endpoint(self) -> str:
        return self.BASE_ENDPOINT

    def create_from(self, params: TokenData) -> Token:
        self.assert_private_key_is_set()

        customer_info = params.customer_info.to_dict() if params.customer_info else None

        response = self.api_service.post(
            self.create_endpoint(),
            json={
                "pri_key": self.api_service.private_key,
                "amount": params.amount,
                "currency": params.currency,
                "order_id": params.order_id,
                "success_url": params.success_url,
                "error_url": params.error_url,
                "customer_ip": params.customer_ip,
                "customer": customer_info,
                "metadata": params.metadata,
            },
        )

        self.assert_response(response)
        response_data = response.get("token")
        return Token.create_from_dict(response_data)

    def assert_response(self, response: Response):
        if response.status_code == 200:
            if not isinstance(response.get("token"), dict) or "id" not in response.get(
                "token"
            ):
                raise MissingTokenException("Missing token in response")
            return

        if response.status_code in [404, 422]:
            message = response.get("message")
            if response.get("success") is False and isinstance(message, str):
                raise ValidationException(message)

            if response.status_code == 422:
                raise UnexpectedResultException("Unexpected result from server")

        elif 500 <= response.status_code < 600:
            raise ServerException("Internal server error")

        else:
            raise UnsupportedResponseException("Unsupported response status code")
