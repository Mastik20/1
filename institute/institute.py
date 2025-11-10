"""Institute aggregates courses across the organization."""

from __future__ import annotations

from typing import Iterable, List

from .course import Course
from .university_entity import UniversityEntity


class Institute(UniversityEntity):
    """Represent an entire institute containing multiple courses."""

    def __init__(self, name: str, courses: Iterable[Course] | None = None) -> None:
        super().__init__(name)
        self._courses: List[Course] = []
        if courses:
            for course in courses:
                self.add_course(course)

    @property
    def courses(self) -> tuple[Course, ...]:
        """Return an immutable view of the institute's courses."""

        return tuple(self._courses)

    def add_course(self, course: Course) -> None:
        """Add a course to the institute."""

        if any(existing.number == course.number for existing in self._courses):
            raise ValueError(
                f"Course number {course.number} already exists in the institute."
            )
        self._courses.append(course)

    def remove_course(self, number: int) -> None:
        """Remove a course identified by its number."""

        for index, existing in enumerate(self._courses):
            if existing.number == number:
                del self._courses[index]
                return
        raise ValueError(f"Course number {number} not found in the institute.")

    def __str__(self) -> str:
        course_descriptions = ", ".join(str(course) for course in self._courses) or "no courses"
        return f"Institute {self.name}: {len(self._courses)} courses ({course_descriptions})"
