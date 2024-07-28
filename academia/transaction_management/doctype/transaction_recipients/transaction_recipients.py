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

		has_sign: DF.Check
		is_received: DF.Check
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		print_paper: DF.Check
		recipient_company: DF.Link
		recipient_department: DF.Link | None
		recipient_designation: DF.Link | None
		recipient_email: DF.Link
		recipient_name: DF.Data | None
		step: DF.Int
	# end: auto-generated types
	pass
