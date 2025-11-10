"""Institute domain model package."""
from .course import Course
from .data_manager import DataManager
from .department import Department
from .faculty import Faculty
from .group import Group
from .institute import Institute
from .student import Student
from .university_entity import UniversityEntity

__all__ = [
    "Course",
    "DataManager",
    "Department",
    "Faculty",
    "Group",
    "Institute",
    "Student",
    "UniversityEntity",
]
