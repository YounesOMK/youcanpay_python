import unittest
from unittest.mock import Mock
from youcanpay_python.api.endpoints import KeysEndpoint, TokenEndpoint

from youcanpay_python.api.service import APIService
from youcanpay_python.exceptions.exceptions import (
    ServerException,
    UnsupportedResponseException,
)
from youcanpay_python.models.data import Response
from youcanpay_python.models.token import TokenData


class TestAPIService(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_adapter_picker = Mock()
        self.mock_adapter = Mock()
        self.mock_adapter_picker.pick.return_value = self.mock_adapter

        self.api_service = APIService(self.mock_adapter_picker)

    def test_init(self):
        self.mock_adapter_picker.pick.assert_called_once_with(False)
        self.assertEqual(self.api_service.http_adapter, self.mock_adapter)

    def test_use_keys(self):
        self.api_service.use_keys("pri_key", "pub_key")
        self.assertEqual(self.api_service.private_key, "pri_key")
        self.assertEqual(self.api_service.public_key, "pub_key")

    def test_get(self):
        self.api_service.get("endpoint", param="value")
        self.mock_adapter.get.assert_called_once_with("endpoint", param="value")

    def test_post(self):
        self.api_service.post("endpoint", param="value")
        self.mock_adapter.post.assert_called_once_with("endpoint", param="value")


class TestKeysEndpoint(unittest.TestCase):
    def setUp(self):
        self.mock_api_service = Mock(spec=APIService)
        self.keys_endpoint = KeysEndpoint(self.mock_api_service)

    def test_endpoint(self):
        self.assertEqual(self.keys_endpoint.endpoint(), "keys")

    def test_check_with_keys(self):
        self.mock_api_service.post.return_value = Response(200, [])
        result = self.keys_endpoint.check(private_key="pri_key", public_key="pub_key")
        self.assertTrue(result)

    def test_check_with_incorrect_keys(self):
        self.mock_api_service.post.return_value = Response(401, [])
        result = self.keys_endpoint.check(private_key="pri_key", public_key="pub_key")
        self.assertFalse(result)

    def test_check_with_server_error(self):
        self.mock_api_service.post.return_value = Response(500, [])
        with self.assertRaises(ServerException):
            self.keys_endpoint.check(private_key="pri_key", public_key="pub_key")


class TestTokenEndpoint(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_api_service = Mock(spec=APIService)
        self.token_endpoint = TokenEndpoint(self.mock_api_service)

    def test_endpoint(self):
        self.assertEqual(self.token_endpoint.endpoint(), "tokenize")

    def test_create_from_valid_data(self):
        self.mock_api_service.private_key = "pri_key"
        self.mock_api_service.public_key = "pri_key"

        self.mock_api_service.post.return_value = Response(
            200, {"token": {"id": "token_id"}}
        )
        mock_token_data = TokenData(
            order_id="ord123", amount="2", currency="MAD", customer_ip="123.123.123"
        )

        token = self.token_endpoint.create_from(mock_token_data)
        self.assertIsNotNone(token)

    def test_create_from_invalid_data(self):
        self.mock_api_service.private_key = "pri_key"
        self.mock_api_service.public_key = "pri_key"

        self.mock_api_service.post.return_value = Response(401, {"token": {}})
        mock_token_data = TokenData(
            order_id="ord123", amount="2", currency="MAD", customer_ip="123.123.123"
        )

        with self.assertRaises(UnsupportedResponseException):
            self.token_endpoint.create_from(mock_token_data)
