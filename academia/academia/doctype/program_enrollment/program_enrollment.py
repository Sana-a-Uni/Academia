# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ProgramEnrollment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_term: DF.Link | None
		academic_year: DF.Link
		enrollment_date: DF.Date | None
		faculty: DF.Link
		image: DF.AttachImage | None
		program: DF.Link
		status: DF.Link | None
		student: DF.Link
		student_batch: DF.Link | None
		student_name: DF.Data | None
	# end: auto-generated types
	pass
