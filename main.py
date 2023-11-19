from ipaddress import ip_address
from models.data import Customer
from youcan_pay import YouCanPay
from models.token import TokenData


if __name__ == "__main__":
    YouCanPay.enable_sandbox_mode()

    you_can_pay = YouCanPay.instance().use_keys(
        "pri_key",
        "pub_key",
    )

    # Example customer information
    customer_info = Customer(
        name="Younes",
        address="123 street",
        zip_code="999",
        country_code="MA",
        phone="+212600000000",
        email="example@example.com",
    )

    # Example metadata for the transaction
    metadata = {"item_id": "A123", "campaign": "Summer Sale"}

    # Order details
    token_params = TokenData(
        order_id="OR238472",
        amount="2000",
        currency="MAD",
        customer_ip="123.123.123.123",
        success_url="https://example.com/success",
        error_url="https://example.com/error",
        customer_info=customer_info,
        metadata=metadata,
    )

    # Create the token and return the payment URL
    token = you_can_pay.token.create_from(token_params)
    print(token.get_payment_url())
