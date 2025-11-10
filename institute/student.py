"""Domain model for students within the institute."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Student:
    """Represent an individual student."""

    first_name: str
    last_name: str
    student_id: str
    average_grade: float

    def __post_init__(self) -> None:
        if not self.first_name or not self.last_name:
            raise ValueError("Student first and last names must be non-empty.")
        if not self.student_id:
            raise ValueError("Student ID must be provided.")
        if not 0.0 <= self.average_grade <= 100.0:
            raise ValueError("Average grade must be between 0.0 and 100.0.")

    def __str__(self) -> str:
        return (
            f"Student {self.first_name} {self.last_name} "
            f"(ID: {self.student_id}, GPA: {self.average_grade:.2f})"
        )
