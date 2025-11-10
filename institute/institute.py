"""Institute aggregate entity."""
from __future__ import annotations

from typing import Iterable, List, Optional

from .course import Course
from .department import Department
from .faculty import Faculty
from .group import Group
from .student import Student
from .university_entity import UniversityEntity


class Institute(UniversityEntity):
    """Represent an institute containing multiple courses."""

    def __init__(self, name: str, courses: Iterable[Course] | None = None) -> None:
        super().__init__(name)
        self._courses: List[Course] = []
        if courses:
            for course in courses:
                self.add_course(course)

    @property
    def courses(self) -> tuple[Course, ...]:
        return tuple(self._courses)

    def add_course(self, course: Course) -> None:
        if not isinstance(course, Course):
            raise TypeError("course must be an instance of Course")
        if any(existing.number == course.number for existing in self._courses):
            raise ValueError(f"Course with number {course.number} already exists in {self.name}")
        self._courses.append(course)

    def remove_course(self, number: int) -> Course:
        for index, course in enumerate(self._courses):
            if course.number == number:
                return self._courses.pop(index)
        raise ValueError(f"Course with number {number} not found in {self.name}")

    def find_course(self, number: int) -> Optional[Course]:
        """Return a course by number if present."""
        return next((course for course in self._courses if course.number == number), None)

    def find_faculty(self, name: str) -> Optional[tuple[Course, Faculty]]:
        for course in self._courses:
            faculty = course.find_faculty(name)
            if faculty:
                return course, faculty
        return None

    def find_department(self, name: str) -> Optional[tuple[Course, Faculty, Department]]:
        for course in self._courses:
            for faculty in course.faculties:
                department = faculty.find_department(name)
                if department:
                    return course, faculty, department
        return None

    def find_group(self, name: str) -> Optional[tuple[Course, Faculty, Department, Group]]:
        for course in self._courses:
            for faculty in course.faculties:
                for department in faculty.departments:
                    group = department.find_group(name)
                    if group:
                        return course, faculty, department, group
        return None

    def find_student_by_id(
        self, student_id: str
    ) -> Optional[tuple[Course, Faculty, Department, Group, Student]]:
        for course in self._courses:
            for faculty in course.faculties:
                for department in faculty.departments:
                    for group in department.groups:
                        student = group.find_student_by_id(student_id)
                        if student:
                            return course, faculty, department, group, student
        return None

    def find_students_by_name(
        self, name_fragment: str
    ) -> list[tuple[Course, Faculty, Department, Group, Student]]:
        matches: list[tuple[Course, Faculty, Department, Group, Student]] = []
        for course in self._courses:
            for faculty in course.faculties:
                for department in faculty.departments:
                    for group in department.groups:
                        for student in group.find_students_by_name(name_fragment):
                            matches.append((course, faculty, department, group, student))
        return matches

    def __str__(self) -> str:
        course_info = ", ".join(str(course) for course in self._courses) or "no courses"
        return f"Institute {self.name} offering: {course_info}"

    def to_dict(self) -> dict[str, object]:
        """Serialize the institute to a JSON-compatible dictionary."""
        return {
            "name": self.name,
            "courses": [course.to_dict() for course in self._courses],
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Institute":
        """Create an institute from a serialized dictionary."""
        courses_data = data.get("courses", [])
        courses = [Course.from_dict(course_data) for course_data in courses_data]
        return cls(name=str(data["name"]), courses=courses)
