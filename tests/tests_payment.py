import unittest
from unittest.mock import Mock, patch
from youcanpay_python.api.endpoints import KeysEndpoint, TokenEndpoint

from youcanpay_python.api.service import APIService
from youcanpay_python.youcan_pay import YouCanPay


class TestYouCanPay(unittest.TestCase):
    def setUp(self):
        self.mock_api_service = Mock(spec=APIService)
        self.mock_keys_endpoint = Mock(spec=KeysEndpoint)
        self.mock_token_endpoint = Mock(spec=TokenEndpoint)

        with patch(
            "youcanpay_python.api.endpoints.KeysEndpoint",
            return_value=self.mock_keys_endpoint,
        ):
            with patch(
                "youcanpay_python.api.endpoints.TokenEndpoint",
                return_value=self.mock_token_endpoint,
            ):
                self.youcanpay = YouCanPay(self.mock_api_service)

    def test_init_endpoints(self):
        self.assertIsInstance(self.youcanpay.token, TokenEndpoint)
        self.assertIsInstance(self.youcanpay.keys, KeysEndpoint)

    def test_use_keys(self):
        private_key, public_key = "private_key", "public_key"
        self.youcanpay.use_keys(private_key, public_key)
        self.mock_api_service.use_keys.assert_called_with(private_key, public_key)
        self.assertIsInstance(self.youcanpay.token, TokenEndpoint)
        self.assertIsInstance(self.youcanpay.keys, KeysEndpoint)

    @patch("youcanpay_python.api.service.APIService")
    @patch("youcanpay_python.adapters.adapter_picker.HttpAdapterPicker")
    def test_instance_class_method(self, mock_adapter_picker, mock_api_service):
        instance = YouCanPay.instance()
        self.assertIsInstance(instance, YouCanPay)

    @patch("youcanpay_python.api.service.APIService.is_sandbox_mode", new=True)
    def test_enable_sandbox_mode_class_method(self):
        YouCanPay.enable_sandbox_mode()
        self.assertTrue(APIService.is_sandbox_mode)

    @patch("youcanpay_python.api.service.APIService.is_sandbox_mode", new=False)
    def test_sandbox_mode_class_method(self):
        YouCanPay.instance()
        self.assertFalse(APIService.is_sandbox_mode)
