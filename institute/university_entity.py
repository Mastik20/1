"""Base class for university entities."""
from __future__ import annotations

from abc import ABC


class UniversityEntity(ABC):
    """Abstract base class that stores a name for a university entity."""

    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("name cannot be empty or whitespace")
        self._name = cleaned_name

    @property
    def name(self) -> str:
        """Return the entity name."""
        return self._name

    def __str__(self) -> str:  # pragma: no cover - trivial override point
        return f"{self.__class__.__name__}: {self.name}"
