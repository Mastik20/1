"""Faculty aggregates multiple departments."""

from __future__ import annotations

from typing import Iterable, List

from .department import Department
from .university_entity import UniversityEntity


class Faculty(UniversityEntity):
    """Represent a faculty containing several departments."""

    def __init__(self, name: str, departments: Iterable[Department] | None = None) -> None:
        super().__init__(name)
        self._departments: List[Department] = []
        if departments:
            for department in departments:
                self.add_department(department)

    @property
    def departments(self) -> tuple[Department, ...]:
        """Return an immutable view of the faculty's departments."""

        return tuple(self._departments)

    def add_department(self, department: Department) -> None:
        """Add a department to the faculty."""

        if any(existing.name == department.name for existing in self._departments):
            raise ValueError(
                f"Department {department.name} already exists in faculty {self.name}."
            )
        self._departments.append(department)

    def remove_department(self, name: str) -> None:
        """Remove a department identified by its name."""

        for index, existing in enumerate(self._departments):
            if existing.name == name:
                del self._departments[index]
                return
        raise ValueError(f"Department {name} not found in faculty {self.name}.")

    def __str__(self) -> str:
        return f"Faculty {self.name}: {len(self._departments)} departments"
