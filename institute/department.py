"""Department entity definition."""
from __future__ import annotations

from typing import Iterable, List, Optional

from .group import Group
from .university_entity import UniversityEntity


class Department(UniversityEntity):
    """Represent an academic department."""

    def __init__(self, name: str, groups: Iterable[Group] | None = None) -> None:
        super().__init__(name)
        self._groups: List[Group] = []
        if groups:
            for group in groups:
                self.add_group(group)

    @property
    def groups(self) -> tuple[Group, ...]:
        return tuple(self._groups)

    def add_group(self, group: Group) -> None:
        if not isinstance(group, Group):
            raise TypeError("group must be an instance of Group")
        if any(existing.name == group.name for existing in self._groups):
            raise ValueError(f"Group with name {group.name} already exists in department {self.name}")
        self._groups.append(group)

    def remove_group(self, name: str) -> Group:
        for index, group in enumerate(self._groups):
            if group.name == name:
                return self._groups.pop(index)
        raise ValueError(f"Group with name {name} not found in department {self.name}")

    def find_group(self, name: str) -> Optional[Group]:
        """Return a group by name if present."""
        return next((group for group in self._groups if group.name == name), None)

    def __str__(self) -> str:
        return f"Department {self.name} with {len(self._groups)} groups"

    def to_dict(self) -> dict[str, object]:
        """Serialize the department to a JSON-compatible dictionary."""
        return {
            "name": self.name,
            "groups": [group.to_dict() for group in self._groups],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Department":
        """Create a department from a serialized dictionary."""
        groups_data = data.get("groups", [])
        groups = [Group.from_dict(group_data) for group_data in groups_data]
        return cls(name=str(data["name"]), groups=groups)
