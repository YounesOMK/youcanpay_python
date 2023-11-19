import os
import unittest
from unittest.mock import Mock, patch

from youcanpay_python.adapters.http_adapters import RequestsHttpAdapter


class TestRequestsHttpAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = RequestsHttpAdapter(is_sandbox_mode=False)

    def test_api_url_sandbox_mode(self):
        sandbox_adapter = RequestsHttpAdapter(is_sandbox_mode=True)
        expected_url = "https://youcanpay.com/sandbox/api/"
        self.assertEqual(sandbox_adapter.api_url, expected_url)

    def test_api_url_production_mode(self):
        expected_url = "https://youcanpay.com/api/"
        self.assertEqual(self.adapter.api_url, expected_url)

    @patch.dict(os.environ, {"YOUCAN_PAY_URL": "https://customurl.com/"})
    def test_api_url_with_env_variable(self):
        custom_url_adapter = RequestsHttpAdapter(is_sandbox_mode=False)
        expected_url = "https://customurl.com/api/"
        self.assertEqual(custom_url_adapter.api_url, expected_url)

    def test_api_url_without_env_variable(self):
        with patch.dict("os.environ", {}, clear=True):
            adapter = RequestsHttpAdapter(is_sandbox_mode=False)
            expected_url = "https://youcanpay.com/api/"
            self.assertEqual(adapter.api_url, expected_url)

    @patch("requests.request")
    def test_make_request(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "some_data"}
        mock_request.return_value = mock_response

        response = self.adapter.make_request("GET", "endpoint")

        mock_request.assert_called_with(
            "GET", "https://youcanpay.com/api/endpoint", **{}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"data": "some_data"})
