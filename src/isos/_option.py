from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, TypeVar, Generic, override, final, TYPE_CHECKING

if TYPE_CHECKING:
    from ._result import Result

from ._error import UNWRAP_OPTION_MSG, UnwrapError
from ._util import Ord, NotComparableError

T = TypeVar("T")
W = TypeVar("W")


@dataclass
class Option(ABC, Generic[T]):
    def less_than(self, other: Option[W]) -> Result[bool]:
        """
        Return True if this Option is strictly less than `other`.
        If the contained values (for `Some`) are not mutually comparable via
        the `<` operator, it returns a `NotComparable` error.
        """
        from ._result import Ok, Err

        try:
            is_less = self.less_than_unsafe(other)
            return Ok(is_less)
        except Exception as _:
            return Err(NotComparableError())

    def less_or_equal(self, other: Option[W]) -> Result[bool]:
        """
        Return True if this Option is less than or equal to `other`.
        If the contained values (for `Some`) are not mutually comparable via
        the `<` operator, it returns a `NotComparable` error.
        """
        from ._result import Ok, Err

        try:
            is_less_or_equal = self.less_or_equal_unsafe(other)
            return Ok(is_less_or_equal)
        except Exception as _:
            return Err(NotComparableError())

    def greater_than(self, other: Option[W]) -> Result[bool]:
        """
        Return True if this Option is strictly greater than `other`.
        If the contained values (for `Some`) are not mutually comparable via
        the `<` operator, it returns a `NotComparable` error.
        """
        from ._result import Ok, Err

        try:
            is_greater = self.greater_than_unsafe(other)
            return Ok(is_greater)
        except Exception as _:
            return Err(NotComparableError())

    def greater_or_equal(self, other: Option[W]) -> Result[bool]:
        """
        Return True if this Option is greater than or equal to `other`.
        If the contained values (for `Some`) are not mutually comparable via
        the `<` operator, it returns a `NotComparable` error.
        """
        from ._result import Ok, Err

        try:
            is_greater_or_equal = self.greater_or_equal_unsafe(other)
            return Ok(is_greater_or_equal)
        except Exception as _:
            return Err(NotComparableError())

    @abstractmethod
    def less_than_unsafe(self, other: Option[W]) -> bool:
        """
        Return True if this Option is strictly less than `other`.

        This method is *unsafe* in the sense that it assumes the contained
        values (for `Some`) are mutually comparable via the `<` operator.
        """
        raise NotImplementedError("The method is not implemented")

    def less_or_equal_unsafe(self, other: Option[W]) -> bool:
        """
        Return True if this Option is less than or equal to `other`.

        This method is *unsafe* in the sense that it assumes the contained
        values (for `Some`) are mutually comparable via the `<` operator.
        """
        return self.less_than_unsafe(other) or self == other

    def greater_than_unsafe(self, other: Option[W]) -> bool:
        """
        Return True if this Option is strictly greater than `other`.

        This method is *unsafe* in the sense that it assumes the contained
        values (for `Some`) are mutually comparable via the `<` operator.
        """
        return not self.less_or_equal_unsafe(other)

    def greater_or_equal_unsafe(self, other: Option[W]) -> bool:
        """
        Return True if this Option is greater or equal to `other`.

        This method is *unsafe* in the sense that it assumes the contained
        values (for `Some`) are mutually comparable via the `<` operator.
        """
        return not self.less_than_unsafe(other)

    def is_some(self) -> bool:
        return not self.is_none()

    @abstractmethod
    def is_some_and(self, f: Callable[[T], bool]) -> bool:
        """
        Returns `True` if the the option is a `Some` and its value matches
        a predicate.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def is_none(self) -> bool:
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def is_none_or(self, f: Callable[[T], bool]) -> bool:
        """
        Returns `True` if the option is a `None` or the value inside of it matches
        a predicate.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def expect(self, msg: str) -> T:
        """
        Returns the contained `Some` value or raises an exception with a custom
        message.
        """
        raise NotImplementedError("The method is not implemented")

    def unwrap(self) -> T:
        """Returns the contained `Some` value or raises an exception."""
        return self.expect(UNWRAP_OPTION_MSG)

    @abstractmethod
    def unwrap_or(self, val: T) -> T:
        """Returns the contained `Some` value or a specified default value."""
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        """Returns the contained `Some` value or a specified value."""
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def map(self, f: Callable[[T], W]) -> Option[W]:
        """
        Maps an Option[T] to Option[W] by applying a function to a contained value
        (if Some) or returns None (if None).
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def map_or(self, default: W, f: Callable[[T], W]) -> W:
        """
        Returns the provided default result (if none), or applies a function to
        the contained value (if any).
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def map_or_else(self, d: Callable[[], W], f: Callable[[T], W]) -> W:
        """
        Computes a default function result (if none), or applies a different function
        to the contained value (if any).
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def and_option(self, optb: Option[T]) -> Option[T]:
        """Returns None if the option is None, otherwise returns optb."""
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def and_then(self, f: Callable[[T], Option[W]]) -> Option[W]:
        """
        Returns None if the option is None, otherwise calls f with the wrapped value
        and returns the result.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def filter(self, p: Callable[[T], bool]) -> Option[T]:
        """
        Returns None if the option is None, otherwise calls predicate with the wrapped
        value and returns:

            - Some(t) if predicate returns true (where t is the wrapped value), and
            - None if predicate returns false.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def or_option(self, optb: Option[T]) -> Option[T]:
        """Returns the option if it contains a value, otherwise returns optb."""
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def or_else(self, f: Callable[[], Option[T]]) -> Option[T]:
        """
        Returns the option if it contains a value, otherwise calls f and returns the result.
        """
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def xor(self, other: Option[T]) -> Option[T]:
        """Returns Some if exactly one of self, optb is Some, otherwise returns None."""
        raise NotImplementedError("The method is not implemented")

    @abstractmethod
    def zip(self, other: Option[W]) -> Option[tuple[T, W]]:
        """
        Zips self with another Option.

        If self is Some(s) and other is Some(o), this method returns Some((s, o)).
        Otherwise, None is returned.
        """
        raise NotImplementedError("The method is not implemented")


@final
@dataclass
class Some(Option[T]):
    inner: T

    @override
    def less_than_unsafe(self, other: Option[W]) -> bool:
        if not isinstance(other, Some) and not isinstance(other, Null):
            raise NotImplementedError(
                "Comparison between Option and other types is not defined."
            )
        if isinstance(other, Null):
            return False
        if isinstance(self.inner, Ord) and isinstance(other.inner, Ord):
            return self.inner < other.inner
        else:
            raise TypeError(f"{T} does not implement __lt__.")

    @override
    def is_some_and(self, f: Callable[[T], bool]) -> bool:
        """
        Returns `True` if the the option is a `Some` and its value matches
        a predicate.
        """
        return f(self.inner)

    @override
    def is_none(self) -> bool:
        return False

    @override
    def is_none_or(self, f: Callable[[T], bool]) -> bool:
        """
        Returns `True` if the option is a `None` or the value inside of it matches
        a predicate.
        """
        return f(self.inner)

    @override
    def expect(self, msg: str) -> T:
        """
        Returns the contained `Some` value or raises an exception with a custom
        message.
        """
        return self.inner

    @override
    def unwrap_or(self, val: T) -> T:
        """Returns the contained `Some` value or a specified default value."""
        return self.inner

    @override
    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        """Returns the contained `Some` value or a specified value."""
        return self.inner

    @override
    def map(self, f: Callable[[T], W]) -> Option[W]:
        """
        Maps an Option[T] to Option[W] by applying a function to a contained value
        (if Some) or returns None (if None).
        """
        return Some(f(self.inner))

    @override
    def map_or(self, default: W, f: Callable[[T], W]) -> W:
        """
        Returns the provided default result (if none), or applies a function to
        the contained value (if any).
        """
        return f(self.inner)

    @override
    def map_or_else(self, d: Callable[[], W], f: Callable[[T], W]) -> W:
        """
        Computes a default function result (if none), or applies a different function
        to the contained value (if any).
        """
        return f(self.inner)

    @override
    def and_option(self, optb: Option[T]) -> Option[T]:
        """Returns None if the option is None, otherwise returns optb."""
        return optb

    @override
    def and_then(self, f: Callable[[T], Option[W]]) -> Option[W]:
        """
        Returns None if the option is None, otherwise calls f with the wrapped value
        and returns the result.
        """
        return f(self.inner)

    @override
    def filter(self, p: Callable[[T], bool]) -> Option[T]:
        """
        Returns None if the option is None, otherwise calls predicate with the wrapped
        value and returns:

            - Some(t) if predicate returns true (where t is the wrapped value), and
            - None if predicate returns false.
        """
        return self if p(self.inner) else Null()

    @override
    def or_option(self, optb: Option[T]) -> Option[T]:
        """Returns the option if it contains a value, otherwise returns optb."""
        return self

    @override
    def or_else(self, f: Callable[[], Option[T]]) -> Option[T]:
        """
        Returns the option if it contains a value, otherwise calls f and returns the result.
        """
        return self

    @override
    def xor(self, other: Option[T]) -> Option[T]:
        """Returns Some if exactly one of self, optb is Some, otherwise returns None."""
        if isinstance(other, Some):  # Both Some
            return Null()
        else:
            return Some(self.inner)

    @override
    def zip(self, other: Option[W]) -> Option[tuple[T, W]]:
        """
        Zips self with another Option.

        If self is Some(s) and other is Some(o), this method returns Some((s, o)).
        Otherwise, None is returned.
        """
        if isinstance(other, Some):
            return Some((self.inner, other.inner))
        else:
            return Null()


@final
@dataclass
class Null(Option[T]):
    @override
    def less_than_unsafe(self, other: object) -> bool:
        if not isinstance(other, Null) and not isinstance(other, Some):
            raise NotImplementedError(
                "Comparison between Option and other types is not defined."
            )
        return not isinstance(other, Null)

    @override
    def is_some_and(self, f: Callable[[T], bool]) -> bool:
        """
        Returns `True` if the the option is a `Some` and its value matches
        a predicate.
        """
        return False

    @override
    def is_none(self) -> bool:
        return True

    @override
    def is_none_or(self, f: Callable[[T], bool]) -> bool:
        """
        Returns `True` if the option is a `None` or the value inside of it matches
        a predicate.
        """
        return True

    @override
    def expect(self, msg: str) -> T:
        """
        Returns the contained `Some` value or raises an exception with a custom
        message.
        """
        raise UnwrapError(msg)

    @override
    def unwrap_or(self, val: T) -> T:
        """Returns the contained `Some` value or a specified default value."""
        return val

    @override
    def unwrap_or_else(self, f: Callable[[], T]) -> T:
        """Returns the contained `Some` value or a specified value."""
        return f()

    @override
    def map(self, f: Callable[[T], W]) -> Option[W]:
        """
        Maps an Option[T] to Option[W] by applying a function to a contained value
        (if Some) or returns None (if None).
        """
        return Null[W]()

    @override
    def map_or(self, default: W, f: Callable[[T], W]) -> W:
        """
        Returns the provided default result (if none), or applies a function to
        the contained value (if any).
        """
        return default

    @override
    def map_or_else(self, d: Callable[[], W], f: Callable[[T], W]) -> W:
        """
        Computes a default function result (if none), or applies a different function
        to the contained value (if any).
        """
        return d()

    @override
    def and_option(self, optb: Option[T]) -> Option[T]:
        """Returns None if the option is None, otherwise returns optb."""
        return self

    @override
    def and_then(self, f: Callable[[T], Option[W]]) -> Option[W]:
        """
        Returns None if the option is None, otherwise calls f with the wrapped value
        and returns the result.
        """
        return Null()

    @override
    def filter(self, p: Callable[[T], bool]) -> Option[T]:
        """
        Returns None if the option is None, otherwise calls predicate with the wrapped
        value and returns:

            - Some(t) if predicate returns true (where t is the wrapped value), and
            - None if predicate returns false.
        """
        return Null()

    @override
    def or_option(self, optb: Option[T]) -> Option[T]:
        """Returns the option if it contains a value, otherwise returns optb."""
        return optb

    @override
    def or_else(self, f: Callable[[], Option[T]]) -> Option[T]:
        """
        Returns the option if it contains a value, otherwise calls f and returns the result.
        """
        return f()

    @override
    def xor(self, other: Option[T]) -> Option[T]:
        """Returns Some if exactly one of self, optb is Some, otherwise returns None."""
        if isinstance(other, Null):  # Both None
            return Null()
        else:
            return other

    @override
    def zip(self, other: Option[W]) -> Option[tuple[T, W]]:
        return Null()


def take(opt: Option[T]) -> tuple[Option[T], Option[T]]:
    """Takes the value from the option leaving None behind."""
    if isinstance(opt, Some):
        return Null(), opt
    return Null(), Null()


def take_if(
    opt: Option[T], f: Callable[[T], bool]
) -> tuple[Option[T], Option[T]]:
    """
    Takes the value out of the option, but only if the predicate evaluates to true
    on the value.

    In other words, replaces self with None if the predicate returns true. This method
    operates similar to Option::take but conditional.
    """
    if isinstance(opt, Some):
        if f(opt.inner):
            return Null(), opt
        else:
            return opt, Null()
    else:
        return Null(), Null()


def replace(opt: Option[T], val: T) -> tuple[Option[T], Option[T]]:
    """
    Replaces the actual value in the option by the value given in parameter, returning
    the old value if present, leaving a Some in its place without deinitializing either one.
    """
    if isinstance(opt, Some):
        return Some(val), opt
    else:
        return Null(), Null()
