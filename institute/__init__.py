"""Convenient exports for the institute domain model."""

from .course import Course
from .department import Department
from .faculty import Faculty
from .group import Group
from .institute import Institute
from .student import Student
from .university_entity import UniversityEntity

__all__ = [
    "Course",
    "Department",
    "Faculty",
    "Group",
    "Institute",
    "Student",
    "UniversityEntity",
]
