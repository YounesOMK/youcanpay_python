from dataclasses import asdict, dataclass
from typing import Any, Optional


@dataclass
class Response:
    status_code: int
    data: Any

    def get(self, key: str) -> Any:
        if isinstance(self.data, dict):
            return self.data.get(key)
        return None


@dataclass
class Customer:
    name: Optional[str] = None
    address: Optional[str] = None
    zip_code: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    def to_dict(self):
        return asdict(self)
