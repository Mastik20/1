"""Group entity definition."""
from __future__ import annotations

from typing import Iterable, List, Optional

from .student import Student
from .university_entity import UniversityEntity


class Group(UniversityEntity):
    """Represent a student group."""

    def __init__(self, name: str, students: Iterable[Student] | None = None) -> None:
        super().__init__(name)
        self._students: List[Student] = []
        if students:
            for student in students:
                self.add_student(student)

    @property
    def students(self) -> tuple[Student, ...]:
        """Return students as an immutable tuple."""
        return tuple(self._students)

    def add_student(self, student: Student) -> None:
        """Add a student to the group, preventing duplicates."""
        if not isinstance(student, Student):
            raise TypeError("student must be an instance of Student")
        if any(existing.student_id == student.student_id for existing in self._students):
            raise ValueError(f"Student with id {student.student_id} already exists in group {self.name}")
        self._students.append(student)

    def remove_student(self, student_id: str) -> Student:
        """Remove and return a student by ID."""
        for index, student in enumerate(self._students):
            if student.student_id == student_id:
                return self._students.pop(index)
        raise ValueError(f"Student with id {student_id} not found in group {self.name}")

    def find_student_by_id(self, student_id: str) -> Optional[Student]:
        """Return a student by ID if present."""
        return next((student for student in self._students if student.student_id == student_id), None)

    def find_students_by_name(self, name_fragment: str) -> list[Student]:
        """Return students whose full name contains the fragment (case-insensitive)."""
        fragment = name_fragment.lower()
        return [student for student in self._students if fragment in student.full_name.lower()]

    def update_student_grade(self, student_id: str, new_grade: float) -> Student:
        """Update the average grade for a specific student."""
        student = self.find_student_by_id(student_id)
        if not student:
            raise ValueError(f"Student with id {student_id} not found in group {self.name}")
        student.update_average_grade(new_grade)
        return student

    def __str__(self) -> str:
        return f"Group {self.name} with {len(self._students)} students"

    def to_dict(self) -> dict[str, object]:
        """Serialize the group to a JSON-compatible dictionary."""
        return {
            "name": self.name,
            "students": [student.to_dict() for student in self._students],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Group":
        """Create a group from a serialized dictionary."""
        students_data = data.get("students", [])
        students = [Student.from_dict(student_data) for student_data in students_data]
        return cls(name=str(data["name"]), students=students)
