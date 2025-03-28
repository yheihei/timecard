from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")

class IEquatable(ABC, Generic[T]):

    @abstractmethod
    def equals(self, other: T) -> bool:
        pass