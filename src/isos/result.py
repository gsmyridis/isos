from __future__ import annotations
from typing import TypeVar, Union, Callable
from dataclasses import dataclass

from .error import UNWRAP_RESULT_MSG, UNWRAP_ERR_RESULT_MSG, UnwrapError, Error
from .option import Option, Some, Null

T = TypeVar("T")
U = TypeVar("U")


@dataclass
class Result[T]:
    inner: Union[T, Error]

    @classmethod
    def Ok(cls, val: T):
        return cls(val)

    @classmethod
    def Err(cls, error: Error):
        return cls(error)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Result):
            raise NotImplementedError(
                "Comparison between Result and other types is not defined."
            )
        return self.inner == other.inner

    def __neq__(self, other: object) -> bool:
        return not self == other

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Result):
            raise NotImplementedError(
                "Comparison between Result and other types is not defined."
            )

        if isinstance(self.inner, Error) and not isinstance(other.inner, Error):
            return True
        elif not isinstance(self.inner, Error) and not isinstance(
            other.inner, Error
        ):
            return self.inner < other.inner
        elif not isinstance(self.inner, Error) and isinstance(
            other.inner, Error
        ):
            return False
        else:
            return False

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Result):
            raise NotImplementedError(
                "Comparison between Result and other types is not defined."
            )
        return self < other or self == other

    def __gt__(self, other: object) -> bool:
        return not self <= other

    def __ge__(self, other: object) -> bool:
        return not self < other

    def is_ok(self) -> bool:
        """Returns `True` if the result is an `Ok`."""
        return False if isinstance(self.inner, Error) else True

    def is_ok_and(self, f: Callable[[T], bool]) -> bool:
        """Returns `True` if the result is an `Ok` and the value satisfies the predicate `f`."""
        if isinstance(self.inner, Error):
            return False
        else:
            return f(self.inner)

    def is_error(self) -> bool:
        """Return `True` if the result is an `Error`."""
        return not self.is_ok()

    def is_error_and(self, f: Callable[[Error], bool]) -> bool:
        """Returns `True` if the result is an `Err` and the value satisfies the predicate `f`."""
        if isinstance(self.inner, Error):
            return f(self.inner)
        else:
            return False

    def ok(self) -> Option[T]:
        """
        Converts from Result[T, E] to Option[T].
        Converts self into an Option[T], and discarding the error, if any.
        """
        if isinstance(self.inner, Error):
            return Null
        else:
            return Some(self.inner)

    def error(self) -> Option[T]:
        """
        Converts from Result[T, E] to Option[E].
        Converts self into an Option[E] and discarding the success value, if any.
        """
        if isinstance(self.inner, Error):
            return Option(self.inner)
        else:
            return Null

    def map(self, f: Callable[[T], U]) -> Result[U]:
        """
        Maps a `Result[T]` to `Result[U]` by applying a function to a contained Ok value,
        leaving an `Error` value untouched.

        This function can be used to compose the results of two functions.
        """
        if not isinstance(self.inner, Error):
            return Result(f(self.inner))
        else:
            return Result(self.inner)

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        """
        Maps a `Result[T]` to `U` by applying a function to a contained Ok value,
        or a default function to an `Error` value.
        """
        if isinstance(self.inner, Error):
            return default
        else:
            return f(self.inner)

    def map_or_else(
        self, default: Callable[[Error], U], f: Callable[[T], U]
    ) -> U:
        """
        Maps a `Result[T]` to U by applying a function to a contained Ok value,
        or a default function to an `Error` value.
        """
        if not isinstance(self.inner, Error):
            return f(self.inner)
        else:
            return default(self.inner)

    def map_error(self, f: Callable[[Error], Error]) -> Result[T]:
        """
        Maps a `Result[T]` to `Result[T]` by applying a function to a contained `Error` value,
        leaving an Ok value untouched.

        This function can be used to pass through a successful result while handling an error.
        """
        if isinstance(self.inner, Error):
            return Result(f(self.inner))
        else:
            return Result(self.inner)

    def expect(self, msg: str) -> T:
        """
        Returns the contained Ok value. If the contained value is `Error`, it throws an
        `UnwrapError` exception with the provided message.
        """
        if isinstance(self.inner, Error):
            raise UnwrapError(msg)
        else:
            return self.inner

    def unwrap(self) -> T:
        """
        Returns the contained Ok value. If the contained value is `Error`, it throws an
        `UnwrapError` exception.
        """
        return self.expect(UNWRAP_RESULT_MSG)

    def expect_error(self, msg: str) -> Error:
        """
        Returns the contained `Error` value. If the contained value is Ok, it throws an
        `UnwrapError` exception with the provided message.
        """
        if isinstance(self.inner, Error):
            return self.inner
        else:
            raise UnwrapError(msg)

    def unwrap_error(self) -> Error:
        """
        Returns the contained `Error` value. If the contained value is Ok, it throws an
        `UnwrapError` exception.
        """
        return self.expect_error(UNWRAP_ERR_RESULT_MSG)

    def unwrap_or(self, default: T) -> T:
        """Returns the contained Ok value or a default value."""
        if isinstance(self.inner, Error):
            return default
        else:
            return self.inner

    def unwrap_or_else(self, f: Callable[[Error], T]) -> T:
        """Returns the contained Ok value or it computes it with a function."""
        if isinstance(self.inner, Error):
            return f(self.inner)
        else:
            return self.inner

    def and_result(self, res: Result[U]) -> Result[U]:
        """
        Returns `res` if the result is Ok, otherwise returns the `Error` value of `self`.
        """
        if isinstance(self.inner, Error):
            return Result(self.inner)
        else:
            return res

    def and_then(self, f: Callable[[T], Result[U]]) -> Result[U]:
        """
        Calls `f` if the result is Ok, otherwise returns the `Error` value of `self`.
        """
        if isinstance(self.inner, Error):
            return Result(self.inner)
        else:
            return f(self.inner)

    def or_result(self, res: Result[T]) -> Result[T]:
        """
        Returns `res` if the result is an `Error`, otherwise returns the Ok value of `self`.
        """
        if isinstance(self.inner, Error):
            return res
        else:
            return Result(self.inner)

    def or_else(self, f: Callable[[Error], Result[T]]) -> Result[T]:
        """
        Calls `f` if the result is an `Error`, otherwise returns the Ok value of `self`.
        """
        if isinstance(self.inner, Error):
            return f(self.inner)
        else:
            return Result(self.inner)


def Ok(val: T) -> Result[T]:
    return Result.Ok(val)


def Err(error: Error) -> Result:
    return Result.Err(error)
