from __future__ import annotations
from typing import TypeVar, Callable, Generic, override, cast
from dataclasses import dataclass
from abc import ABC, abstractmethod

from ._error import UNWRAP_RESULT_MSG, UNWRAP_ERR_RESULT_MSG, UnwrapError, Error
from ._option import Option, Some, Null
from ._util import Ord, NotComparableError

T = TypeVar("T")
U = TypeVar("U")


@dataclass
class Result(ABC, Generic[T]):
    def less_than(self, other: Result[U]) -> Result[bool]:
        """
        Return True if this Result is strictly less than `other`.
        If the contained values (for `Ok`) are not mutually comparable via
        the `<` operator, it returns a `NotComparable` error.
        """
        try:
            is_less = self.less_than_unsafe(other)
            return Ok(is_less)
        except Exception as _:
            return Err(NotComparableError())

    def less_or_equal(self, other: Result[U]) -> Result[bool]:
        """
        Return True if this Result is less than or equal to `other`.
        If the contained values (for `Ok`) are not mutually comparable via
        the `<` operator, it returns a `NotComparable` error.
        """
        try:
            is_less_or_equal = self.less_or_equal_unsafe(other)
            return Ok(is_less_or_equal)
        except Exception as _:
            return Err(NotComparableError())

    def greater_than(self, other: Result[U]) -> Result[bool]:
        """
        Return True if this Result is strictly greater than `other`.
        If the contained values (for `Ok`) are not mutually comparable via
        the `<` operator, it returns a `NotComparable` error.
        """
        try:
            is_greater = self.greater_than_unsafe(other)
            return Ok(is_greater)
        except Exception as _:
            return Err(NotComparableError())

    def greater_or_equal(self, other: Result[U]) -> Result[bool]:
        """
        Return True if this Result is greater than or equal to `other`.
        If the contained values (for `Ok`) are not mutually comparable via
        the `<` operator, it returns a `NotComparable` error.
        """
        try:
            is_greater_or_equal = self.greater_or_equal_unsafe(other)
            return Ok(is_greater_or_equal)
        except Exception as _:
            return Err(NotComparableError())

    @abstractmethod
    def less_than_unsafe(self, other: Result[U]) -> bool:
        """
        Return True if this Result is strictly less than `other`.

        This method is *unsafe* in the sense that it assumes the contained
        values (for `Ok`) are mutually comparable via the `<` operator.
        """
        raise NotImplementedError("The method is not implemented")

    def less_or_equal_unsafe(self, other: Result[U]) -> bool:
        """
        Return True if this Result is less than or equal to `other`.

        This method is *unsafe* in the sense that it assumes the contained
        values (for `Ok`) are mutually comparable via the `<` operator.
        """
        return self.less_than_unsafe(other) or self == other

    def greater_than_unsafe(self, other: Result[U]) -> bool:
        """
        Return True if this Result is strictly greater than `other`.

        This method is *unsafe* in the sense that it assumes the contained
        values (for `Ok`) are mutually comparable via the `<` operator.
        """
        return not self.less_or_equal_unsafe(other)

    def greater_or_equal_unsafe(self, other: Result[U]) -> bool:
        """
        Return True if this Result is greater or equal to `other`.

        This method is *unsafe* in the sense that it assumes the contained
        values (for `Ok`) are mutually comparable via the `<` operator.
        """
        return not self.less_than_unsafe(other)

    @abstractmethod
    def is_ok(self) -> bool:
        """Returns `True` if the result is an `Ok`."""
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def is_ok_and(self, f: Callable[[T], bool]) -> bool:
        """Returns `True` if the result is an `Ok` and the value satisfies the predicate `f`."""
        raise NotImplementedError("The method is not implemented")

    def is_error(self) -> bool:
        """Return `True` if the result is an `Error`."""
        return not self.is_ok()

    @abstractmethod
    def is_error_and(self, f: Callable[[Error], bool]) -> bool:
        """Returns `True` if the result is an `Err` and the value satisfies the predicate `f`."""
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def ok(self) -> Option[T]:
        """
        Converts from Result[T, E] to Option[T].
        Converts self into an Option[T], and discarding the error, if any.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def error(self) -> Option[Error]:
        """
        Converts from Result[T, E] to Option[E].
        Converts self into an Option[E] and discarding the success value, if any.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def map(self, f: Callable[[T], U]) -> Result[U]:
        """
        Maps a `Result[T]` to `Result[U]` by applying a function to a contained Ok value,
        leaving an `Error` value untouched.

        This function can be used to compose the results of two functions.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        """
        Maps a `Result[T]` to `U` by applying a function to a contained Ok value,
        or a default function to an `Error` value.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def map_or_else(
        self, default: Callable[[Error], U], f: Callable[[T], U]
    ) -> U:
        """
        Maps a `Result[T]` to U by applying a function to a contained Ok value,
        or a default function to an `Error` value.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def map_error(self, f: Callable[[Error], Error]) -> Result[T]:
        """
        Maps a `Result[T]` to `Result[T]` by applying a function to a contained `Error` value,
        leaving an Ok value untouched.

        This function can be used to pass through a successful result while handling an error.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def expect(self, msg: str) -> T:
        """
        Returns the contained Ok value. If the contained value is `Error`, it throws an
        `UnwrapError` exception with the provided message.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def unwrap(self) -> T:
        """
        Returns the contained Ok value. If the contained value is `Error`, it throws an
        `UnwrapError` exception.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def expect_error(self, msg: str) -> Error:
        """
        Returns the contained `Error` value. If the contained value is Ok, it throws an
        `UnwrapError` exception with the provided message.
        """
        raise NotImplementedError("The method is not implemented")

    def unwrap_error(self) -> Error:
        """
        Returns the contained `Error` value. If the contained value is Ok, it throws an
        `UnwrapError` exception.
        """
        return self.expect_error(UNWRAP_ERR_RESULT_MSG)

    @abstractmethod
    def unwrap_or(self, default: T) -> T:
        """Returns the contained Ok value or a default value."""
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def unwrap_or_else(self, f: Callable[[Error], T]) -> T:
        """Returns the contained Ok value or it computes it with a function."""
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def and_result(self, res: Result[U]) -> Result[U]:
        """
        Returns `res` if the result is Ok, otherwise returns the `Error` value of `self`.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def and_then(self, f: Callable[[T], Result[U]]) -> Result[U]:
        """
        Calls `f` if the result is Ok, otherwise returns the `Error` value of `self`.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def or_result(self, res: Result[T]) -> Result[T]:
        """
        Returns `res` if the result is an `Error`, otherwise returns the Ok value of `self`.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def or_else(self, f: Callable[[Error], Result[T]]) -> Result[T]:
        """
        Calls `f` if the result is an `Error`, otherwise returns the Ok value of `self`.
        """
        raise NotImplementedError("The method is not implemented")


@dataclass
class Ok(Result[T]):
    inner: T

    @override
    def less_than_unsafe(self, other: Result[U]) -> bool:
        if not isinstance(other, Ok) and not isinstance(other, Err):
            raise NotImplementedError(
                "Comparison between Result and other types is not defined."
            )
        if isinstance(other, Err):
            return False
        if isinstance(self.inner, Ord) and isinstance(other.inner, Ord):
            return self.inner < other.inner
        else:
            raise TypeError(f"{T} does not implement __lt__.")

    @override
    def is_ok(self) -> bool:
        return True

    @override
    def is_ok_and(self, f: Callable[[T], bool]) -> bool:
        return f(self.inner)

    @override
    def is_error_and(self, f: Callable[[Error], bool]) -> bool:
        return False

    @override
    def ok(self) -> Option[T]:
        return Some(self.inner)

    @override
    def error(self) -> Option[Error]:
        return Null()

    @override
    def map(self, f: Callable[[T], U]) -> Result[U]:
        return Ok(f(self.inner))

    @override
    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return f(self.inner)

    @override
    def map_or_else(
        self, default: Callable[[Error], U], f: Callable[[T], U]
    ) -> U:
        return f(self.inner)

    @override
    def map_error(self, f: Callable[[Error], Error]) -> Result[T]:
        return self

    @override
    def expect(self, msg: str) -> T:
        return self.inner

    @override
    def unwrap(self) -> T:
        return self.inner

    @override
    def expect_error(self, msg: str) -> Error:
        raise UnwrapError(msg)

    @override
    def unwrap_or(self, default: T) -> T:
        return self.inner

    @override
    def unwrap_or_else(self, f: Callable[[Error], T]) -> T:
        return self.inner

    @override
    def and_result(self, res: Result[U]) -> Result[U]:
        return res

    @override
    def and_then(self, f: Callable[[T], Result[U]]) -> Result[U]:
        return f(self.inner)

    @override
    def or_result(self, res: Result[T]) -> Result[T]:
        return self

    @override
    def or_else(self, f: Callable[[Error], Result[T]]) -> Result[T]:
        return self


@dataclass
class Err(Result[T]):
    inner: Error

    @override
    def less_than_unsafe(self, other: object) -> bool:
        if not isinstance(other, Result):
            raise NotImplementedError(
                "Comparison between Result and other types is not defined."
            )
        return isinstance(other, Ok)

    @override
    def is_ok(self) -> bool:
        return False

    @override
    def is_ok_and(self, f: Callable[[T], bool]) -> bool:
        return False

    @override
    def is_error_and(self, f: Callable[[Error], bool]) -> bool:
        return f(self.inner)

    @override
    def ok(self) -> Option[T]:
        return Null()

    @override
    def error(self) -> Option[Error]:
        return Some(self.inner)

    @override
    def map(self, f: Callable[[T], U]) -> Result[U]:
        return cast(Err[U], self)

    @override
    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        return default

    @override
    def map_or_else(
        self, default: Callable[[Error], U], f: Callable[[T], U]
    ) -> U:
        return default(self.inner)

    @override
    def map_error(self, f: Callable[[Error], Error]) -> Result[T]:
        return Err(f(self.inner))

    @override
    def expect(self, msg: str) -> T:
        raise UnwrapError(msg)

    @override
    def expect_error(self, msg: str) -> Error:
        return self.inner

    @override
    def unwrap(self) -> T:
        msg = f"{UNWRAP_RESULT_MSG}: {self.inner.MESSAGE}"
        raise UnwrapError(msg)

    @override
    def unwrap_or(self, default: T) -> T:
        return default

    @override
    def unwrap_or_else(self, f: Callable[[Error], T]) -> T:
        return f(self.inner)

    @override
    def and_result(self, res: Result[U]) -> Result[U]:
        return cast(Err[U], self)

    @override
    def and_then(self, f: Callable[[T], Result[U]]) -> Result[U]:
        return cast(Err[U], self)

    @override
    def or_result(self, res: Result[T]) -> Result[T]:
        return res

    @override
    def or_else(self, f: Callable[[Error], Result[T]]) -> Result[T]:
        return f(self.inner)
