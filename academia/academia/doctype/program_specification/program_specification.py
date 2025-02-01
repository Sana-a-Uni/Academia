# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class ProgramSpecification(Document):
	def get_course_list(self):
		return [
			frappe.get_doc("Course Specification", study_plan_course.course_code)
			for study_plan_course in self.table_ytno
		]

	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.course_language.course_language import CourseLanguage
		from academia.academia.doctype.credit_hours_course.credit_hours_course import CreditHoursCourse
		from academia.academia.doctype.program_elective_course.program_elective_course import (
			ProgramElectiveCourse,
		)
		from academia.academia.doctype.study_plan_course.study_plan_course import StudyPlanCourse
		from frappe.types import DF

		abbr: DF.ReadOnly
		academic_degree: DF.ReadOnly
		academic_system: DF.Literal["", "Semester System", "Credit Hours System", "Annual System"]
		approval_date: DF.Date | None
		course_language: DF.TableMultiSelect[CourseLanguage]
		courses: DF.Check
		date_of_programe_development: DF.Date
		date_of_starting_the_program: DF.Date | None
		delivery_mode: DF.Literal["", "On Campus", "Online"]
		department: DF.ReadOnly
		faculty: DF.ReadOnly
		faculty_elective_course: DF.Table[ProgramElectiveCourse]
		faculty_requirements: DF.Link
		file: DF.Attach | None
		implementation_start_academic_year: DF.Link | None
		maximum_research_period: DF.Int
		minimum_course_average_to_start_research: DF.Data | None
		minimum_research_period: DF.Int
		program_elective_course: DF.Table[ProgramElectiveCourse]
		program_name: DF.Link
		program_name_english: DF.ReadOnly
		research_or_thesis: DF.Check
		table_omcu: DF.Table[CreditHoursCourse]
		table_ytno: DF.Table[StudyPlanCourse]
		total_elective_hours: DF.Int
		total_hours_required_to_award_degree: DF.Int
		university_elective_course: DF.Table[ProgramElectiveCourse]
		university_requirements: DF.Link
	# end: auto-generated types


@frappe.whitelist()
def get_required_courses(doc):
	doc = frappe.parse_json(doc)
	if not doc.get("university_requirements") or not doc.get("faculty_requirements"):
		frappe.throw(
			_("Please select University Requirements and Faculty Requirements before fetching courses.")
		)

	courses = []

	# Fetch courses from University Requirement
	university_requirement = frappe.get_doc("University Requirement", doc.get("university_requirements"))
	if university_requirement and university_requirement.table_rzel:
		for row in university_requirement.table_rzel:
			courses.append(
				{
					"course_code": row.course_code,
					"course_name": row.course_name,
					"course_type": row.course_type,
					"study_level": row.study_level,
					"semester": row.semester,
					"elective": row.elective,
					"source": "University Requirement",
				}
			)

	# Fetch courses from Faculty Requirement
	faculty_requirement = frappe.get_doc("Faculty Requirement", doc.get("faculty_requirements"))
	if faculty_requirement and faculty_requirement.table_fgiz:
		for row in faculty_requirement.table_fgiz:
			courses.append(
				{
					"course_code": row.course_code,
					"course_name": row.course_name,
					"course_type": row.course_type,
					"study_level": row.study_level,
					"semester": row.semester,
					"elective": row.elective,
					"source": "Faculty Requirement",
				}
			)

	# Check if courses exist
	if not courses:
		frappe.throw(_("No courses found in the selected University or Faculty Requirements."))

	return courses


# second try
# @frappe.whitelist()
# def get_required_courses(doc):
#     # إذا كان doc هو نص (string)، سنقوم بتحميل المستند باستخدام frappe.get_doc
#     if isinstance(doc, str):
#         doc = frappe.get_doc("Program Specification", doc)

#     if not doc.get("university_requirements") or not doc.get("faculty_requirements"):
#         frappe.throw(_("Please select University Requirements and Faculty Requirements before fetching courses."))

#     courses = []

#     # Fetch courses from University Requirement
#     university_requirement = frappe.get_doc("University Requirement", doc.get("university_requirements"))
#     if university_requirement and university_requirement.table_rzel:
#         for row in university_requirement.table_rzel:
#             courses.append({
#                 "course_code": row.course_code,
#                 "course_name": row.course_name,
#                 "course_type": row.course_type,
#                 "study_level": row.study_level,
#                 "semester": row.semester,
#                 "elective": row.elective,
#                 "source": "University Requirement"
#             })

#     # Fetch courses from Faculty Requirement
#     faculty_requirement = frappe.get_doc("Faculty Requirement", doc.get("faculty_requirements"))
#     if faculty_requirement and faculty_requirement.table_fgiz:
#         for row in faculty_requirement.table_fgiz:
#             courses.append({
#                 "course_code": row.course_code,
#                 "course_name": row.course_name,
#                 "course_type": row.course_type,
#                 "study_level": row.study_level,
#                 "semester": row.semester,
#                 "elective": row.elective,
#                 "source": "Faculty Requirement"
#             })

#     # Check if courses exist
#     if not courses:
#         frappe.throw(_("No courses found in the selected University or Faculty Requirements."))

#     return courses


# @frappe.whitelist()
# def validate_courses_in_plan(doc):
#     # إذا كان doc هو نص (string)، سنقوم بتحميل المستند باستخدام frappe.get_doc
#     if isinstance(doc, str):
#         doc = frappe.get_doc("Program Specification", doc)

#     # Get the list of required courses
#     required_courses = get_required_courses(doc)

#     # Get the list of courses already in the study plan
#     existing_courses = []
#     for row in doc.table_ytno:
#         existing_courses.append(row.course_code)

#     # Identify missing courses
#     missing_courses = []
#     for course in required_courses:
#         if course["course_code"] not in existing_courses:
#             missing_courses.append(course["course_name"])

#     if missing_courses:
#         frappe.throw(_("The study plan must include the following courses:") + "\n" + "\n".join(missing_courses))
