# Copyright (c) 2024, SanU and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

test_data = {
    "program_name": "_Test Program",
    "description": "_Test Program",
    "course_code": [
        {
            "course_name": "_Test Course 1",
        },
        {
            "course_name": "_Test Course 2",
        },
    ],
}

class TestProgramSpecification(FrappeTestCase):
    def setUp(self):
        make_program_and_linked_courses(
            "_Test Program 1", ["_Test Course 1", "_Test Course 2"]
        )

    def test_get_course_list(self):
        program = frappe.get_doc("Program Specification", "_Test Program 1")
        courses = program.get_course_list()
        self.assertEqual(courses[0].name, "_Test Course 1")
        self.assertEqual(courses[1].name, "_Test Course 2")
        frappe.db.rollback()

    def tearDown(self):
        for dt in ["Program Specification", "Course Specification"]:
            for entry in frappe.get_all(dt):
                frappe.delete_doc(dt, entry.name)

def make_program(name):
    program = frappe.get_doc(
        {
            "doctype": "Program Specification",
            "program_name": name,
            "program_code": name,
            "description": "_test description",
            "is_featured": True,
        }
    ).insert()
    return program.name

def make_program_and_linked_courses(program_name, course_name_list):
    try:
        program = frappe.get_doc("Program Specification", program_name)
    except frappe.DoesNotExistError:
        make_program(program_name)
        program = frappe.get_doc("Program Specification", program_name)
    course_list = [make_course(course_name) for course_name in course_name_list]
    for course in course_list:
        program.append("table_ytno", {"course_code": course, "required": 1})
    program.save()
    return program

def make_course(name):
    course = frappe.get_doc(
        {
            "doctype": "Course Specification",
            "course_name": name,
            "course_code": name,
        }
    ).insert()
    return course.name

def setup_program():
    all_courses_list = [
        {"course_code": course["course_name"]}
        for course in test_data["course_code"]
    ]
    for course in all_courses_list:
        make_course(course["course_code"])

    course_list = [course["course_name"] for course in test_data["course_code"]]
    program = make_program_and_linked_courses(test_data["program_name"], course_list)
    return program
