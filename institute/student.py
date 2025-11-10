"""Student entity definition."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Student:
    """Represent a student within the institute."""

    first_name: str
    last_name: str
    student_id: str
    average_grade: float

    def __post_init__(self) -> None:
        if not self.first_name or not self.first_name.strip():
            raise ValueError("first_name cannot be empty")
        if not self.last_name or not self.last_name.strip():
            raise ValueError("last_name cannot be empty")
        if not self.student_id or not self.student_id.strip():
            raise ValueError("student_id cannot be empty")
        self._validate_grade(self.average_grade)

    @staticmethod
    def _validate_grade(value: float) -> None:
        if not (0.0 <= value <= 100.0):
            raise ValueError("average_grade must be between 0 and 100")

    @property
    def full_name(self) -> str:
        """Return the student's full name."""
        return f"{self.first_name} {self.last_name}"

    def update_average_grade(self, new_grade: float) -> None:
        """Update the student's average grade with validation."""
        self._validate_grade(new_grade)
        self.average_grade = new_grade

    def to_dict(self) -> dict[str, object]:
        """Serialize the student to a JSON-compatible dictionary."""
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "student_id": self.student_id,
            "average_grade": self.average_grade,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Student":
        """Create a student from a serialized dictionary."""
        return cls(
            first_name=str(data["first_name"]),
            last_name=str(data["last_name"]),
            student_id=str(data["student_id"]),
            average_grade=float(data["average_grade"]),
        )

    def __str__(self) -> str:
        return (
            f"Student {self.full_name} (ID: {self.student_id}) - "
            f"Average grade: {self.average_grade:.2f}"
        )
