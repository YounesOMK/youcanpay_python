class BaseException(Exception):
    def __init__(self, message, *args, **kwargs):
        super().__init__(message)
        self.args = args
        self.kwargs = kwargs

    def get_details(self):
        return f"Exception Details: {self.args}, {self.kwargs}"


class UnsetPrivateKeyException(BaseException):
    pass


class UnsetPublicKeyException(BaseException):
    pass


class MissingTokenException(BaseException):
    pass


class ValidationException(BaseException):
    pass


class UnexpectedResultException(BaseException):
    pass


class ServerException(Exception):
    pass


class UnsupportedResponseException(BaseException):
    pass
