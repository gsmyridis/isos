from __future__ import annotations
from typing import TypeVar, Union, Callable
from dataclasses import dataclass

from .error import UNWRAP_RESULT_MSG, UNWRAP_ERR_RESULT_MSG, UnwrapError, Error

T = TypeVar("T")
U = TypeVar("U")


@dataclass
class Result[T]:
    inner: Union[T, Error]

    def is_ok(self) -> bool:
        """Returns `True` if the result is an `Ok`."""
        return False if isinstance(self.inner, Error) else True

    def is_ok_and(self, f: Callable[[T], bool]) -> bool:
        """Returns `True` if the result is an `Ok` and the value satisfies the predicate `f`."""
        if isinstance(self.inner, Error):
            return False
        else:
            return f(self.inner)

    def is_err(self) -> bool:
        """Return `True` if the result is an `Error`."""
        return not self.is_ok()

    def is_err_and(self, f: Callable[[Error], bool]) -> bool:
        """Returns `True` if the result is an `Err` and the value satisfies the predicate `f`."""
        if isinstance(self.inner, Error):
            return f(self.inner)
        else:
            return False

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

    def map_or_else(self, default: Callable[[Error], U], f: Callable[[T], U]) -> U:
        """
        Maps a `Result[T]` to U by applying a function to a contained Ok value,
        or a default function to an `Error` value.
        """
        if not isinstance(self.inner, Error):
            return f(self.inner)
        else:
            return default(self.inner)

    def map_err(self, f: Callable[[Error], Error]) -> Result[T]:
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

    def expect_err(self, msg: str) -> Error:
        """
        Returns the contained `Error` value. If the contained value is Ok, it throws an
        `UnwrapError` exception with the provided message.
        """
        if isinstance(self.inner, Error):
            return self.inner
        else:
            raise UnwrapError(msg)

    def unwrap_err(self) -> Error:
        """
        Returns the contained `Error` value. If the contained value is Ok, it throws an
        `UnwrapError` exception.
        """
        return self.expect_err(UNWRAP_ERR_RESULT_MSG)

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

    def and_(self, res: Result[U]) -> Result[U]:
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

    def or_(self, res: Result[T]) -> Result[T]:
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
