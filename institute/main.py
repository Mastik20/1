"""Console interface for managing an institute."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Optional

from .course import Course
from .data_manager import DataManager
from .department import Department
from .faculty import Faculty
from .group import Group
from .institute import Institute
from .student import Student

DEFAULT_DATA_FILE = Path("institute_data.json")


def prompt_non_empty(message: str, allow_default: bool = False, default: str = "") -> str:
    """Prompt the user until a non-empty value is provided."""
    while True:
        raw_value = input(message).strip()
        if raw_value:
            return raw_value
        if allow_default:
            return default
        print("Value cannot be empty. Please try again.")


def prompt_int(message: str) -> int:
    while True:
        try:
            return int(prompt_non_empty(message))
        except ValueError:
            print("Please enter a valid integer.")


def prompt_float(message: str) -> float:
    while True:
        try:
            return float(prompt_non_empty(message))
        except ValueError:
            print("Please enter a valid number.")


def choose_course(institute: Institute) -> Optional[Course]:
    if not institute.courses:
        print("No courses available. Please add a course first.")
        return None
    number = prompt_int("Enter course number: ")
    course = institute.find_course(number)
    if not course:
        print(f"Course {number} not found.")
    return course


def choose_faculty(institute: Institute) -> Optional[tuple[Course, Faculty]]:
    course = choose_course(institute)
    if not course:
        return None
    if not course.faculties:
        print("No faculties in this course. Please add one first.")
        return None
    faculty_name = prompt_non_empty("Enter faculty name: ")
    faculty = course.find_faculty(faculty_name)
    if not faculty:
        print(f"Faculty '{faculty_name}' not found in course {course.number}.")
        return None
    return course, faculty


def choose_department(institute: Institute) -> Optional[tuple[Course, Faculty, Department]]:
    faculty_path = choose_faculty(institute)
    if not faculty_path:
        return None
    course, faculty = faculty_path
    if not faculty.departments:
        print("No departments in this faculty. Please add one first.")
        return None
    department_name = prompt_non_empty("Enter department name: ")
    department = faculty.find_department(department_name)
    if not department:
        print(f"Department '{department_name}' not found in faculty {faculty.name}.")
        return None
    return course, faculty, department


def choose_group(institute: Institute) -> Optional[tuple[Course, Faculty, Department, Group]]:
    department_path = choose_department(institute)
    if not department_path:
        return None
    course, faculty, department = department_path
    if not department.groups:
        print("No groups in this department. Please add one first.")
        return None
    group_name = prompt_non_empty("Enter group name: ")
    group = department.find_group(group_name)
    if not group:
        print(f"Group '{group_name}' not found in department {department.name}.")
        return None
    return course, faculty, department, group


def add_course(institute: Institute) -> None:
    number = prompt_int("Enter new course number (1-6): ")
    try:
        institute.add_course(Course(number))
        print(f"Added course {number}.")
    except (TypeError, ValueError) as exc:
        print(f"Error adding course: {exc}")


def add_faculty(institute: Institute) -> None:
    course = choose_course(institute)
    if not course:
        return
    name = prompt_non_empty("Enter faculty name: ")
    try:
        course.add_faculty(Faculty(name))
        print(f"Added faculty '{name}' to course {course.number}.")
    except (TypeError, ValueError) as exc:
        print(f"Error adding faculty: {exc}")


def add_department(institute: Institute) -> None:
    faculty_path = choose_faculty(institute)
    if not faculty_path:
        return
    course, faculty = faculty_path
    name = prompt_non_empty("Enter department name: ")
    try:
        faculty.add_department(Department(name))
        print(f"Added department '{name}' to faculty {faculty.name} (course {course.number}).")
    except (TypeError, ValueError) as exc:
        print(f"Error adding department: {exc}")


def add_group(institute: Institute) -> None:
    department_path = choose_department(institute)
    if not department_path:
        return
    course, faculty, department = department_path
    name = prompt_non_empty("Enter group name: ")
    try:
        department.add_group(Group(name))
        print(
            "Added group '{name}' to department {dept} (faculty {fac}, course {course_no}).".format(
                name=name, dept=department.name, fac=faculty.name, course_no=course.number
            )
        )
    except (TypeError, ValueError) as exc:
        print(f"Error adding group: {exc}")


def add_student(institute: Institute) -> None:
    group_path = choose_group(institute)
    if not group_path:
        return
    course, faculty, department, group = group_path
    first_name = prompt_non_empty("Enter student first name: ")
    last_name = prompt_non_empty("Enter student last name: ")
    student_id = prompt_non_empty("Enter student ID: ")
    average_grade = prompt_float("Enter student average grade (0-100): ")
    try:
        student = Student(first_name, last_name, student_id, average_grade)
        group.add_student(student)
        print(
            "Added student {student} to group {group_name} (department {dept}, faculty {fac}, course {course_no}).".format(
                student=student,
                group_name=group.name,
                dept=department.name,
                fac=faculty.name,
                course_no=course.number,
            )
        )
    except (TypeError, ValueError) as exc:
        print(f"Error adding student: {exc}")


def remove_course(institute: Institute) -> None:
    number = prompt_int("Enter course number to remove: ")
    try:
        removed = institute.remove_course(number)
        print(f"Removed {removed}.")
    except ValueError as exc:
        print(exc)


def remove_faculty(institute: Institute) -> None:
    faculty_path = choose_faculty(institute)
    if not faculty_path:
        return
    course, faculty = faculty_path
    course.remove_faculty(faculty.name)
    print(f"Removed faculty '{faculty.name}' from course {course.number}.")


def remove_department(institute: Institute) -> None:
    department_path = choose_department(institute)
    if not department_path:
        return
    course, faculty, department = department_path
    faculty.remove_department(department.name)
    print(f"Removed department '{department.name}' from faculty {faculty.name}.")


def remove_group(institute: Institute) -> None:
    group_path = choose_group(institute)
    if not group_path:
        return
    course, faculty, department, group = group_path
    department.remove_group(group.name)
    print(f"Removed group '{group.name}' from department {department.name}.")


def remove_student(institute: Institute) -> None:
    group_path = choose_group(institute)
    if not group_path:
        return
    *_, group = group_path
    student_id = prompt_non_empty("Enter student ID to remove: ")
    try:
        removed = group.remove_student(student_id)
        print(f"Removed {removed} from group {group.name}.")
    except ValueError as exc:
        print(exc)


def show_structure(institute: Institute) -> None:
    print(f"Institute: {institute.name}")
    if not institute.courses:
        print("  No courses available.")
        return
    for course in institute.courses:
        print(f"  Course {course.number} ({len(course.faculties)} faculties)")
        for faculty in course.faculties:
            print(f"    Faculty {faculty.name} ({len(faculty.departments)} departments)")
            for department in faculty.departments:
                print(f"      Department {department.name} ({len(department.groups)} groups)")
                for group in department.groups:
                    print(f"        Group {group.name} ({len(group.students)} students)")
                    for student in group.students:
                        print(f"          {student}")


def search_menu(institute: Institute) -> None:
    print("Search options:")
    print("  1. Student by ID")
    print("  2. Student by name")
    print("  3. Group by name")
    print("  4. Department by name")
    choice = prompt_non_empty("Select search option: ")
    if choice == "1":
        student_id = prompt_non_empty("Enter student ID: ")
        result = institute.find_student_by_id(student_id)
        if not result:
            print("Student not found.")
            return
        course, faculty, department, group, student = result
        print(
            "Student found: {student} (Group {group}, Department {dept}, Faculty {fac}, Course {course_no})".format(
                student=student,
                group=group.name,
                dept=department.name,
                fac=faculty.name,
                course_no=course.number,
            )
        )
    elif choice == "2":
        fragment = prompt_non_empty("Enter part of the student's name: ")
        matches = institute.find_students_by_name(fragment)
        if not matches:
            print("No students found with that name fragment.")
            return
        for course, faculty, department, group, student in matches:
            print(
                "- {student} (Group {group}, Department {dept}, Faculty {fac}, Course {course_no})".format(
                    student=student,
                    group=group.name,
                    dept=department.name,
                    fac=faculty.name,
                    course_no=course.number,
                )
            )
    elif choice == "3":
        group_name = prompt_non_empty("Enter group name: ")
        result = institute.find_group(group_name)
        if not result:
            print("Group not found.")
            return
        course, faculty, department, group = result
        print(
            "Group found: {group} (Department {dept}, Faculty {fac}, Course {course_no})".format(
                group=group.name,
                dept=department.name,
                fac=faculty.name,
                course_no=course.number,
            )
        )
    elif choice == "4":
        dept_name = prompt_non_empty("Enter department name: ")
        result = institute.find_department(dept_name)
        if not result:
            print("Department not found.")
            return
        course, faculty, department = result
        print(
            "Department found: {dept} (Faculty {fac}, Course {course_no})".format(
                dept=department.name,
                fac=faculty.name,
                course_no=course.number,
            )
        )
    else:
        print("Unknown option.")


def edit_student_grade(institute: Institute) -> None:
    student_id = prompt_non_empty("Enter student ID to edit: ")
    result = institute.find_student_by_id(student_id)
    if not result:
        print("Student not found.")
        return
    course, faculty, department, group, student = result
    new_grade = prompt_float("Enter new average grade (0-100): ")
    try:
        group.update_student_grade(student.student_id, new_grade)
        print(
            "Updated grade for {student} in group {group_name} (department {dept}, faculty {fac}, course {course_no}).".format(
                student=student,
                group_name=group.name,
                dept=department.name,
                fac=faculty.name,
                course_no=course.number,
            )
        )
    except ValueError as exc:
        print(f"Error updating grade: {exc}")


def resolve_file_path(default_path: Path) -> Path:
    raw = input(f"Enter file path [{default_path}]: ").strip()
    if raw:
        return Path(raw).expanduser()
    return default_path.expanduser()


def save_data(institute: Institute, default_path: Path = DEFAULT_DATA_FILE) -> None:
    path = resolve_file_path(default_path)
    try:
        DataManager.save(institute, path)
        print(f"Data saved to {path}.")
    except OSError as exc:
        print(f"Failed to save data: {exc}")


def load_data(default_path: Path = DEFAULT_DATA_FILE) -> Optional[Institute]:
    path = resolve_file_path(default_path)
    try:
        institute = DataManager.load(path)
        print(f"Loaded institute '{institute.name}' from {path}.")
        return institute
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}")
    except (OSError, ValueError) as exc:
        print(f"Failed to load data: {exc}")
    return None


def load_data_action(_: Institute) -> Optional[Institute]:
    """Prompt for a file path and return the loaded institute if successful."""
    return load_data(DEFAULT_DATA_FILE)


def load_initial_institute(default_path: Path) -> Institute:
    path = default_path.expanduser()
    if path.exists():
        try:
            institute = DataManager.load(path)
            print(f"Loaded institute '{institute.name}' from {path}.")
            return institute
        except (json.JSONDecodeError, OSError, ValueError) as exc:
            print(f"Could not load existing data: {exc}")
    name = input("Enter institute name [My Institute]: ").strip() or "My Institute"
    return Institute(name)


def wrap_action(action: Callable[[Institute], None]) -> Callable[[Institute], Optional[Institute]]:
    def wrapper(institute: Institute) -> Optional[Institute]:
        action(institute)
        return None

    return wrapper


def main() -> None:
    institute = load_initial_institute(DEFAULT_DATA_FILE)

    actions: dict[str, Callable[[Institute], Optional[Institute]]] = {
        "1": wrap_action(add_course),
        "2": wrap_action(add_faculty),
        "3": wrap_action(add_department),
        "4": wrap_action(add_group),
        "5": wrap_action(add_student),
        "6": wrap_action(remove_course),
        "7": wrap_action(remove_faculty),
        "8": wrap_action(remove_department),
        "9": wrap_action(remove_group),
        "10": wrap_action(remove_student),
        "11": wrap_action(show_structure),
        "12": wrap_action(search_menu),
        "13": wrap_action(edit_student_grade),
        "14": wrap_action(save_data),
        "15": load_data_action,
    }

    while True:
        print("\nInstitute Management Menu")
        print("-------------------------")
        print(" 1. Add course")
        print(" 2. Add faculty")
        print(" 3. Add department")
        print(" 4. Add group")
        print(" 5. Add student")
        print(" 6. Remove course")
        print(" 7. Remove faculty")
        print(" 8. Remove department")
        print(" 9. Remove group")
        print("10. Remove student")
        print("11. Show institute structure")
        print("12. Search")
        print("13. Edit student average grade")
        print("14. Save data")
        print("15. Load data")
        print(" 0. Exit")
        choice = input("Select an option: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if not action:
            print("Unknown option. Please try again.")
            continue
        result = action(institute)
        if isinstance(result, Institute) and result is not institute:
            institute = result


if __name__ == "__main__":
    main()
