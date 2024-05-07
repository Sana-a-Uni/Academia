# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CourseStudy(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_term: DF.Link
		academic_year: DF.Link
		course_code: DF.Link
		course_name: DF.Data | None
		course_type: DF.ReadOnly | None
		instructor: DF.Link | None
		program: DF.Link
		student_batch: DF.Link
	# end: auto-generated types
	pass
