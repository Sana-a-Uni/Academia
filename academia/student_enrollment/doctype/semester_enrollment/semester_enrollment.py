# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class SemesterEnrollment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.level_and_semester_course.level_and_semester_course import LevelandSemesterCourse
		from frappe.types import DF

		academic_program: DF.Link | None
		academic_year: DF.Link | None
		batch: DF.Link | None
		enrollment_date: DF.Datetime
		faculty: DF.Link | None
		level: DF.Link | None
		level_courses: DF.Table[LevelandSemesterCourse]
		semester: DF.Link | None
		student: DF.Link
		student_name: DF.Data | None
	# end: auto-generated types
	pass
