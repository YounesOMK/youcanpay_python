from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from youcanpay.adapters.http_adapters import BaseHttpAdapter
from youcanpay.api.service import APIService

from youcanpay.models.data import Customer


@dataclass
class TokenData:
    order_id: str
    amount: str
    currency: str
    customer_ip: str
    success_url: Optional[str] = None
    error_url: Optional[str] = None
    customer_info: Optional[Customer] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Token:
    id: str

    @classmethod
    def create_from_dict(cls, attributes: dict):
        if "id" not in attributes:
            raise ValueError("Missing keys in token response")
        return cls(attributes["id"])

    def get_payment_url(self, lang: str = "en") -> str:
        base_url = BaseHttpAdapter.DEFAULT_BASE_APP_URL + (
            "sandbox/" if APIService.is_sandbox_mode else ""
        )
        return f"{base_url}payment-form/{self.id}?lang={lang}"
