# youcanpay_python
![PyPI - Version](https://img.shields.io/pypi/v/youcanpay)
[![Mypy, Black and Tests](https://github.com/YounesOMK/youcanpay_python/actions/workflows/mypy-black-tests.yml/badge.svg?branch=main)](https://github.com/YounesOMK/youcanpay_python/actions/workflows/mypy-black-tests.yml)


Python wrapper arround [YouCanPay gateway](https://youcanpay.com)

## Installation

Install `youcanpay` using pip:

```bash
pip install youcanpay
```

## Usage Example

The following example demonstrates how to use `youcanpay` to create a payment token:

```python
from youcanpay.youcan_pay import YouCanPay
from youcanpay.models.token import TokenData
from youcanpay.models.data import Customer

# Enable sandbox mode for testing
YouCanPay.enable_sandbox_mode()

# Initialize YouCanPay with your private and public keys
youcan_pay = YouCanPay.instance().use_keys(
    "your_private_key",
    "your_public_key",
)

# Set up customer information
customer_info = Customer(
    name="Younes",
    address="123 street",
    zip_code="999",
    country_code="MA",
    phone="+212600000000",
    email="example@example.com",
)

# Define metadata for the transaction
metadata = {"item_id": "A123", "campaign": "Summer Sale"}

# Configure order details
token_params = TokenData(
    order_id="OR238472",
    amount="20",
    currency="USD",
    customer_ip="123.123.123.123",
    success_url="https://example.com/success",
    error_url="https://example.com/error",
    customer_info=customer_info,
    metadata=metadata,
)

# Create the token and get the payment URL
token = youcan_pay.token.create_from(token_params)
payment_url = token.get_payment_url()
