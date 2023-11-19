from youcanpay_python.adapters.http_adapters import RequestsHttpAdapter


class HttpAdapterPicker:
    def pick(self, is_sandbox_mode: bool):
        try:
            import requests

            return RequestsHttpAdapter(is_sandbox_mode)

        except ImportError:
            # TODO later : fallback options
            raise ImportError(
                "The requests library is required but not installed. "
                "Please install it."
            )
