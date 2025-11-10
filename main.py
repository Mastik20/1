"""Demonstrate the institute domain model in action."""

from __future__ import annotations

from institute import Course, Department, Faculty, Group, Institute, Student


def build_sample_institute() -> Institute:
    """Construct a sample institute graph demonstrating the relationships."""

    # Create students and assign them to groups
    group_a = Group(
        "Group A",
        students=[
            Student("Alice", "Anderson", "S001", 92.5),
            Student("Bob", "Baker", "S002", 85.0),
        ],
    )
    group_b = Group(
        "Group B",
        students=[
            Student("Carol", "Clark", "S003", 88.0),
            Student("David", "Doe", "S004", 79.5),
        ],
    )

    # Departments hold groups
    department_math = Department("Mathematics", groups=[group_a])
    department_cs = Department("Computer Science", groups=[group_b])

    # Faculties manage departments
    faculty_science = Faculty("Science", departments=[department_math, department_cs])

    # Courses collect faculties (e.g., for specific academic years)
    course_one = Course(1, faculties=[faculty_science])
    course_two = Course(2)
    course_two.add_faculty(faculty_science)

    # Institute aggregates courses
    institute = Institute("Tech Institute", courses=[course_one])
    institute.add_course(course_two)

    return institute


def main() -> None:
    institute = build_sample_institute()
    print(institute)
    for course in institute.courses:
        print(f"  {course}")
        for faculty in course.faculties:
            print(f"    {faculty}")
            for department in faculty.departments:
                print(f"      {department}")
                for group in department.groups:
                    print(f"        {group}")
                    for student in group.students:
                        print(f"          {student}")


if __name__ == "__main__":
    main()
