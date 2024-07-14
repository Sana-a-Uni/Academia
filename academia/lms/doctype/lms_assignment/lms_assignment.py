# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LMSAssignment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		attachment: DF.Attach | None
		course: DF.Link | None
		from_date: DF.Datetime | None
		instruction: DF.SmallText | None
		make_the_assignment_availability: DF.Check
		question: DF.TextEditor | None
		student_group: DF.Link | None
		title: DF.Data
		to_date: DF.Datetime | None
	# end: auto-generated types
	pass
