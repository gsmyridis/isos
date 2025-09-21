from dataclasses import dataclass
from typing import ClassVar, final, Callable, TypeVar, override

UNWRAP_OPTION_MSG = "Called Option.unwrap() on None."
UNWRAP_RESULT_MSG = "Called Result.unwrap() on Error."
UNWRAP_ERR_RESULT_MSG = "Called Result.unwrap_err() on Ok."

T = TypeVar("T")


@dataclass(frozen=True)
class Error:
    """A class representing an error contained in a Result type."""

    MESSAGE: ClassVar[str]

    @override
    def __str__(self) -> str:
        return self.MESSAGE


class UnwrapError(Exception):
    """Exception raised when trying to unwrap an enum variant with no value."""

    def __init__(self, message: str = ""):
        super().__init__(message)


def error(message: str) -> Callable[[type], type[Error]]:
    def decorator(cls: type) -> type[Error]:
        @final
        class ErrorClass(Error):
            MESSAGE = message

        # Copy the class name
        ErrorClass.__name__ = cls.__name__
        ErrorClass.__qualname__ = cls.__qualname__
        return ErrorClass

    return decorator
