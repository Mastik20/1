"""Groups of students belonging to a department."""

from __future__ import annotations

from typing import Iterable, List

from .student import Student
from .university_entity import UniversityEntity


class Group(UniversityEntity):
    """Represent a group of students."""

    def __init__(self, name: str, students: Iterable[Student] | None = None) -> None:
        super().__init__(name)
        self._students: List[Student] = []
        if students:
            for student in students:
                self.add_student(student)

    @property
    def students(self) -> tuple[Student, ...]:
        """Return a snapshot of the students in the group."""

        return tuple(self._students)

    def add_student(self, student: Student) -> None:
        """Add a student to the group if their ID is unique."""

        if any(existing.student_id == student.student_id for existing in self._students):
            raise ValueError(
                f"Student with ID {student.student_id} already exists in group {self.name}."
            )
        self._students.append(student)

    def remove_student(self, student_id: str) -> None:
        """Remove a student identified by their ID."""

        for index, existing in enumerate(self._students):
            if existing.student_id == student_id:
                del self._students[index]
                return
        raise ValueError(f"Student ID {student_id} not found in group {self.name}.")

    def __str__(self) -> str:
        return f"Group {self.name}: {len(self._students)} students"
