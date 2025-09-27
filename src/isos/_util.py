from __future__ import annotations
from typing import Protocol, runtime_checkable
from ._error import error


@runtime_checkable
class Ord(Protocol):
    def __lt__(self, other: object) -> bool: ...


@error("Values are not mutually comparable")
class NotComparableError: ...
