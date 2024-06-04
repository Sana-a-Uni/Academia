# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class StudyPlanCourse(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		course_code: DF.Link
		course_name: DF.ReadOnly | None
		course_type: DF.ReadOnly | None
		elective: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		semester: DF.Link | None
		study_level: DF.Link | None
	# end: auto-generated types
	pass
