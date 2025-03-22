from __future__ import annotations
from typing import Optional, Callable, Tuple, TypeVar, Generic
from dataclasses import dataclass

from .error import UnwrapError

T = TypeVar("T")
W = TypeVar("W")


@dataclass
class Option(Generic[T]):
    inner: Optional[T]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Option):
            raise NotImplementedError(
                "Comparison between Option and other types is not defined."
            )
        return self.inner == other.inner

    def __neq__(self, other: object) -> bool:
        return not self == other

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Option):
            raise NotImplementedError(
                "Comparison between Option and other types is not defined."
            )

        if self.inner is None and other.inner is not None:
            return True
        elif self.inner is not None and other.inner is not None:
            return self.inner < other.inner
        elif self.inner is not None and other.inner is None:
            return False
        else:
            return False

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Option):
            raise NotImplementedError(
                "Comparison between Option and other types is not defined."
            )
        return self < other or self == other

    def __gt__(self, other: object) -> bool:
        return not self <= other

    def __ge__(self, other: object) -> bool:
        return not self < other

    @classmethod
    def none(cls) -> Option[T]:
        return Option(None)

    @classmethod
    def some(cls, val: T) -> Option[T]:
        return Option(val)

    def is_some(self) -> bool:
        return not self.is_none()

    def is_some_and(self, f: Callable[[T], bool]) -> bool:
        """
        Returns `True` if the the option is a `Some` and its value matches
        a predicate.
        """
        return False if self.inner is None else f(self.inner)

    def is_none(self) -> bool:
        return self.inner is None

    def is_none_or(self, f: Callable[[T], bool]) -> bool:
        """
        Returns `True` if the option is a `None` or the value inside of it matches
        a predicate.
        """
        return self.inner is None or f(self.inner)

    def expect(self, msg: str) -> T:
        """
        Returns the contained `Some` value or raises an exception with a custom
        message.
        """
        if self.inner is None:
            raise UnwrapError(f"{msg}")
        else:
            return self.inner

    def unwrap(self) -> T:
        """Returns the contained `Some` value or raises an exception."""
        return self.expect("Cannot unwrap option that is None.")

    def unwrap_or(self, val: T) -> T:
        """Returns the contained `Some` value or a specified default value."""
        return val if self.inner is None else self.inner

    def unwrap_or_else(self, f: Callable[[], T]):
        """Returns the contained `Some` value or a specified value."""
        return f() if self.inner is None else self.inner

    def map(self, f: Callable[[T], W]) -> Option[W]:
        """
        Maps an Option[T] to Option[W] by applying a function to a contained value
        (if Some) or returns None (if None).
        """
        return Option(None) if self.inner is None else Option(f(self.inner))

    def map_or(self, default: W, f: Callable[[T], W]) -> W:
        """
        Returns the provided default result (if none), or applies a function to
        the contained value (if any).
        """
        return default if self.inner is None else f(self.inner)

    def map_or_else(self, d: Callable[[], W], f: Callable[[T], W]) -> W:
        """
        Computes a default function result (if none), or applies a different function
        to the contained value (if any).
        """
        return d() if self.inner is None else f(self.inner)

    def and_(self, optb: Option[T]) -> Option[T]:
        """Returns None if the option is None, otherwise returns optb."""
        return Option(None) if self.inner is None else optb

    def and_then(self, f: Callable[[T], Option[W]]) -> Option[W]:
        """
        Returns None if the option is None, otherwise calls f with the wrapped value
        and returns the result.
        """
        return Option(None) if self.inner is None else f(self.inner)

    def filter(self, p: Callable[[T], bool]) -> Option[T]:
        """
        Returns None if the option is None, otherwise calls predicate with the wrapped
        value and returns:

            - Some(t) if predicate returns true (where t is the wrapped value), and
            - None if predicate returns false.
        """
        return Option(None) if (self.inner is None or not p(self.inner)) else self

    def or_(self, optb: Option[T]) -> Option[T]:
        """Returns the option if it contains a value, otherwise returns optb."""
        return optb if self.inner is None else self

    def or_else(self, f: Callable[[], Option[T]]) -> Option[T]:
        """
        Returns the option if it contains a value, otherwise calls f and returns the result.
        """
        return f() if self.inner is None else self

    def xor(self, other: Option[T]) -> Option[T]:
        """Returns Some if exactly one of self, optb is Some, otherwise returns None."""
        if self.inner is None and other.inner is None:  # Both None
            return Option(None)
        elif self.inner is not None and other.inner is not None:  # Both Some
            return Option(None)
        elif self.inner is not None:
            return self
        else:
            return other

    def insert(self, value: T):
        """Inserts a value into the Option. If the option had a value, it's dropped."""
        if value is None:
            raise ValueError("Value cannot be not None.")
        self.inner = value

    def get_or_insert(self, value: T) -> None:
        """
        Inserts value into the option if it is None, then returns a mutable reference
        to the contained value.
        """
        raise NotImplementedError("The method has not been implemented yet.")

    def take(self) -> Option[T]:
        """Takes the value from the option leaving None behind."""
        val = self.inner
        self.inner = None
        return Option(val)

    def take_if(self, f: Callable[[T], bool]) -> Option[T]:
        """
        Takes the value out of the option, but only if the predicate evaluates to true
        on the value.

        In other words, replaces self with None if the predicate returns true. This method
        operates similar to Option::take but conditional.
        """
        if self.inner is None:
            return Option(None)
        elif f(self.inner):
            val = self.inner
            self.inner = None
            return Option(val)

        return Option(None)

    def replace(self, val: T) -> Option[T]:
        """
        Replaces the actual value in the option by the value given in parameter, returning
        the old value if present, leaving a Some in its place without deinitializing either one.
        """
        ret = self.inner
        self.inner = val
        return Option(ret)

    def zip(self, other: Option[W]) -> Option[Tuple[T, W]]:
        """
        Zips self with another Option.

        If self is Some(s) and other is Some(o), this method returns Some((s, o)).
        Otherwise, None is returned.
        """
        if self.inner is not None and other.inner is not None:
            return Option((self.inner, other.inner))
        else:
            return Option(None)
