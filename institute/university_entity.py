"""Common abstractions for institute domain entities."""

from __future__ import annotations


class UniversityEntity:
    """Base class representing an institute entity with a human-readable name."""

    def __init__(self, name: str) -> None:
        if not name:
            raise ValueError("Name must be a non-empty string.")
        self._name = name

    @property
    def name(self) -> str:
        """Return the display name of the entity."""

        return self._name

    def __str__(self) -> str:  # pragma: no cover - subclasses provide details
        return self._name
