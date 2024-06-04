# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CourseSchedule(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_term: DF.Link
		academic_year: DF.Link
		course: DF.Link
		group: DF.Data | None
		instructor: DF.Link
		level: DF.Link
		program: DF.Link
		room: DF.Link
	# end: auto-generated types
	pass
