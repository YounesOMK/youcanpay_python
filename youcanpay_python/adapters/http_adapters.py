from abc import ABC, abstractmethod
import os
from urllib.parse import urljoin

from youcanpay_python.models.data import Response


class BaseHttpAdapter(ABC):
    DEFAULT_BASE_APP_URL: str = "https://youcanpay.com/"

    def __init__(self, is_sandbox_mode: bool):
        self.is_sandbox_mode = is_sandbox_mode

    @property
    def api_url(self) -> str:
        base_url = os.getenv("YOUCAN_PAY_URL", self.DEFAULT_BASE_APP_URL)
        api_path = "sandbox/api/" if self.is_sandbox_mode else "api/"

        return urljoin(base_url, api_path)

    @abstractmethod
    def make_request(self, method: str, endpoint: str, **kwargs) -> Response:
        pass


class RequestsHttpAdapter(BaseHttpAdapter):
    def get(self, endpoint: str, **kwargs) -> Response:
        return self.make_request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Response:
        return self.make_request("POST", endpoint, **kwargs)

    def make_request(self, method: str, endpoint: str, **kwargs):
        from requests import request

        url = urljoin(self.api_url, endpoint)
        response = request(method, url, **kwargs)
        return Response(response.status_code, response.json())
