"""Course entity definition."""
from __future__ import annotations

from typing import Iterable, List, Optional

from .faculty import Faculty
from .university_entity import UniversityEntity


class Course(UniversityEntity):
    """Represent a course year within the institute."""

    def __init__(self, number: int, faculties: Iterable[Faculty] | None = None) -> None:
        if not isinstance(number, int):
            raise TypeError("number must be an integer")
        if not 1 <= number <= 6:
            raise ValueError("number must be between 1 and 6")
        super().__init__(f"Course {number}")
        self._number = number
        self._faculties: List[Faculty] = []
        if faculties:
            for faculty in faculties:
                self.add_faculty(faculty)

    @property
    def number(self) -> int:
        return self._number

    @property
    def faculties(self) -> tuple[Faculty, ...]:
        return tuple(self._faculties)

    def add_faculty(self, faculty: Faculty) -> None:
        if not isinstance(faculty, Faculty):
            raise TypeError("faculty must be an instance of Faculty")
        if any(existing.name == faculty.name for existing in self._faculties):
            raise ValueError(
                f"Faculty with name {faculty.name} already exists in course {self._number}"
            )
        self._faculties.append(faculty)

    def remove_faculty(self, name: str) -> Faculty:
        for index, faculty in enumerate(self._faculties):
            if faculty.name == name:
                return self._faculties.pop(index)
        raise ValueError(f"Faculty with name {name} not found in course {self._number}")

    def find_faculty(self, name: str) -> Optional[Faculty]:
        """Return a faculty by name if present."""
        return next((faculty for faculty in self._faculties if faculty.name == name), None)

    def __str__(self) -> str:
        return f"Course {self._number} with {len(self._faculties)} faculties"

    def to_dict(self) -> dict[str, object]:
        """Serialize the course to a JSON-compatible dictionary."""
        return {
            "number": self._number,
            "faculties": [faculty.to_dict() for faculty in self._faculties],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Course":
        """Create a course from a serialized dictionary."""
        faculties_data = data.get("faculties", [])
        faculties = [Faculty.from_dict(faculty_data) for faculty_data in faculties_data]
        return cls(number=int(data["number"]), faculties=faculties)
