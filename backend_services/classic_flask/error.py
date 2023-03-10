from http import HTTPStatus


class APIError(Exception):
    """
    Base class for the custom exceptions, that the application can raise
    """
    def __init__(self, http_status: HTTPStatus, error_params=None, message=None):
        self._http_status = http_status
        if message is not None:
            self._error_msg = message
        else:
            self._error_msg = f"API raised {self.__class__.__name__} exception"
        self._error_attributes = error_params if error_params is not None else {}

    @property
    def message(self) -> str:
        return self._error_msg

    @property
    def attributes(self) -> dict:
        return self._error_attributes

    @property
    def http_status(self) -> HTTPStatus:
        return self._http_status

