# Copyright (c) 2025, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Signatures(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		employee_designation: DF.Data | None
		employee_name: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
	# end: auto-generated types
	pass
