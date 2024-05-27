# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CourseEnrollment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_program: DF.Link
		academic_year: DF.Link
		course: DF.Link | None
		enrollment_date: DF.Date
		faculty: DF.Link
		faculty_department: DF.Link
		semester: DF.Link | None
		student: DF.Link
		student_batch: DF.Link
		student_name: DF.Data | None
	# end: auto-generated types
	pass
