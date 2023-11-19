from typing import Optional
from youcanpay.adapters.adapter_picker import HttpAdapterPicker
from youcanpay.models.data import Response


class APIService:
    # shared
    is_sandbox_mode: bool = False

    def __init__(self, adapter_picker: HttpAdapterPicker):
        self.http_adapter = adapter_picker.pick(APIService.is_sandbox_mode)
        self.private_key: Optional[str] = None
        self.public_key: Optional[str] = None

    def use_keys(self, private_key: str, public_key: str):
        self.private_key = private_key
        self.public_key = public_key

    def get(self, endpoint: str, **kwargs) -> Response:
        return self.http_adapter.get(endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Response:
        return self.http_adapter.post(endpoint, **kwargs)
