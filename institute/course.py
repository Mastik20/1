"""Courses tie faculties to a specific academic year."""

from __future__ import annotations

from typing import Iterable, List

from .faculty import Faculty
from .university_entity import UniversityEntity


class Course(UniversityEntity):
    """Represent a course year, containing multiple faculties."""

    def __init__(self, number: int, faculties: Iterable[Faculty] | None = None) -> None:
        if not 1 <= number <= 6:
            raise ValueError("Course number must be between 1 and 6.")
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
        """Return an immutable view of the course's faculties."""

        return tuple(self._faculties)

    def add_faculty(self, faculty: Faculty) -> None:
        """Add a faculty to the course."""

        if any(existing.name == faculty.name for existing in self._faculties):
            raise ValueError(f"Faculty {faculty.name} already exists in course {self.number}.")
        self._faculties.append(faculty)

    def remove_faculty(self, name: str) -> None:
        """Remove a faculty identified by its name."""

        for index, existing in enumerate(self._faculties):
            if existing.name == name:
                del self._faculties[index]
                return
        raise ValueError(f"Faculty {name} not found in course {self.number}.")

    def __str__(self) -> str:
        return f"Course {self.number}: {len(self._faculties)} faculties"
