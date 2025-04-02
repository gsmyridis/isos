from dataclasses import dataclass


@dataclass
class Error:
    """A class representing an error contained in a Result type."""

    _msg: str = ""

    def get_message(self) -> str:
        return self._msg

    def __str__(self) -> str:
        return self._msg


class UnwrapError(Exception):
    """Exception raised when trying to unwrap an enum variant with no value."""

    pass


UNWRAP_OPTION_MSG = "Called Option.unwrap() on None."
UNWRAP_RESULT_MSG = "Called Result.unwrap() on Error."
UNWRAP_ERR_RESULT_MSG = "Called Result.unwrap_err() on Ok."
