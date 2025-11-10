"""Departments manage groups within a faculty."""

from __future__ import annotations

from typing import Iterable, List

from .group import Group
from .university_entity import UniversityEntity


class Department(UniversityEntity):
    """Represent an academic department overseeing multiple groups."""

    def __init__(self, name: str, groups: Iterable[Group] | None = None) -> None:
        super().__init__(name)
        self._groups: List[Group] = []
        if groups:
            for group in groups:
                self.add_group(group)

    @property
    def groups(self) -> tuple[Group, ...]:
        """Return an immutable view of the department's groups."""

        return tuple(self._groups)

    def add_group(self, group: Group) -> None:
        """Add a group to the department."""

        if any(existing.name == group.name for existing in self._groups):
            raise ValueError(f"Group {group.name} already exists in department {self.name}.")
        self._groups.append(group)

    def remove_group(self, name: str) -> None:
        """Remove a group identified by its name."""

        for index, existing in enumerate(self._groups):
            if existing.name == name:
                del self._groups[index]
                return
        raise ValueError(f"Group {name} not found in department {self.name}.")

    def __str__(self) -> str:
        return f"Department {self.name}: {len(self._groups)} groups"
