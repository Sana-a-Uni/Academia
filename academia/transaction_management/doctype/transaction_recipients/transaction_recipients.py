# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class TransactionRecipients(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		fully_electronic: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		recipient_company: DF.Link | None
		recipient_department: DF.Link | None
		recipient_designation: DF.Link | None
		recipient_email: DF.Link | None
		recipient_name: DF.Data | None
		step: DF.Int
	# end: auto-generated types
	pass
