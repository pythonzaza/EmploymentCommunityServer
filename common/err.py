from typing import Any, Sequence
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorList


class HTTPException(Exception):

    def __init__(self, message: str, status: int, data=''):
        self.message: str = message
        self.status: int = status
        self.data: Any = data


class ValidationException(RequestValidationError):

    def __init__(self, errors: Sequence[ErrorList], *, message: str, status: int, data: Any, body: Any = None) -> None:
        self.message: str = message
        self.status: int = status
        self.data: Any = data
        super().__init__(errors, body=body)
