# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class lab(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		acceptable_increase: DF.Data | None
		building: DF.Link | None
		description: DF.TextEditor | None
		faculty: DF.Link
		lab_name: DF.Data
		lab_type: DF.Link
		seating_capacity: DF.Data | None
	# end: auto-generated types
	pass
