# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AcademicTerm(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_year: DF.Link
		auto_created: DF.Check
		disabled: DF.Check
		exam_end: DF.Date | None
		exam_start: DF.Date | None
		faculty: DF.Link
		study_end: DF.Date | None
		study_start: DF.Date | None
		term_name: DF.Data
	# end: auto-generated types
	pass
