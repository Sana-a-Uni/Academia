# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CourseEnrollmentTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.course_enrollment_course.course_enrollment_course import CourseEnrollmentCourse
		from frappe.types import DF

		academic_program: DF.Literal["", "All Program", "Specific Program"]
		academic_term: DF.Link
		academic_year: DF.Link
		current_level: DF.ReadOnly
		level: DF.Literal["", "All Level", "Specific Level"]
		program_specification: DF.ReadOnly | None
		specific_level: DF.Link | None
		specific_program: DF.Link | None
		student_batch: DF.Link
		table_yztw: DF.Table[CourseEnrollmentCourse]
	# end: auto-generated types
	pass
