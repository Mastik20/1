"""Faculty entity definition."""
from __future__ import annotations

from typing import Iterable, List, Optional

from .department import Department
from .university_entity import UniversityEntity


class Faculty(UniversityEntity):
    """Represent a faculty."""

    def __init__(self, name: str, departments: Iterable[Department] | None = None) -> None:
        super().__init__(name)
        self._departments: List[Department] = []
        if departments:
            for department in departments:
                self.add_department(department)

    @property
    def departments(self) -> tuple[Department, ...]:
        return tuple(self._departments)

    def add_department(self, department: Department) -> None:
        if not isinstance(department, Department):
            raise TypeError("department must be an instance of Department")
        if any(existing.name == department.name for existing in self._departments):
            raise ValueError(
                f"Department with name {department.name} already exists in faculty {self.name}"
            )
        self._departments.append(department)

    def remove_department(self, name: str) -> Department:
        for index, department in enumerate(self._departments):
            if department.name == name:
                return self._departments.pop(index)
        raise ValueError(f"Department with name {name} not found in faculty {self.name}")

    def find_department(self, name: str) -> Optional[Department]:
        """Return a department by name if present."""
        return next((department for department in self._departments if department.name == name), None)

    def __str__(self) -> str:
        return f"Faculty {self.name} with {len(self._departments)} departments"

    def to_dict(self) -> dict[str, object]:
        """Serialize the faculty to a JSON-compatible dictionary."""
        return {
            "name": self.name,
            "departments": [department.to_dict() for department in self._departments],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Faculty":
        """Create a faculty from a serialized dictionary."""
        departments_data = data.get("departments", [])
        departments = [Department.from_dict(dept_data) for dept_data in departments_data]
        return cls(name=str(data["name"]), departments=departments)
