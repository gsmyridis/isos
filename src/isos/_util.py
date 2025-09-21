from __future__ import annotations
from typing import Protocol, runtime_checkable


@runtime_checkable
class Ord(Protocol):
    def __lt__(self, other: object) -> bool: ...
