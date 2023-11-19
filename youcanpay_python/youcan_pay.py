from youcanpay_python.adapters.adapter_picker import HttpAdapterPicker
from youcanpay_python.api.endpoints import KeysEndpoint, TokenEndpoint
from youcanpay_python.api.service import APIService


class YouCanPay:
    def __init__(self, api_service: APIService):
        self.api_service = api_service
        self.init_endpoints(api_service)

    def init_endpoints(self, api_service: APIService):
        self.token = TokenEndpoint(api_service)
        self.keys = KeysEndpoint(api_service)

    def use_keys(self, private_key: str, public_key: str):
        self.api_service.use_keys(private_key, public_key)
        self.init_endpoints(self.api_service)
        return self

    @classmethod
    def instance(cls):
        return cls(APIService(HttpAdapterPicker()))

    @classmethod
    def enable_sandbox_mode(cls):
        APIService.is_sandbox_mode = True

    def check_keys(self, private_key: str, public_key: str):
        return self.keys.check(private_key=private_key, public_key=public_key)
