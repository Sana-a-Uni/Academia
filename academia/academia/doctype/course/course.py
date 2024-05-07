# Copyright (c) 2023, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Course(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		course_code: DF.Data
		course_image: DF.AttachImage | None
		course_name: DF.Data
		course_name_english: DF.Data
		course_type: DF.Literal["", "University Requirement", "Faculty Requirement", "Program Requirement"]
		description: DF.TextEditor | None
		elective_template: DF.Check
		faculty: DF.Link | None
		program: DF.Link | None
	# end: auto-generated types
	pass
