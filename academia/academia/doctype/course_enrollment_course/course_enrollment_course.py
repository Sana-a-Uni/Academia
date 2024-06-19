# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CourseEnrollmentCourse(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		course_code: DF.Link
		course_type: DF.Data | None
		level: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		program: DF.Data | None
	# end: auto-generated types
	pass
