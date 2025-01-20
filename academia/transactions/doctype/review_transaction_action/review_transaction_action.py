# Copyright (c) 2025, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ReviewTransactionAction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action_date: DF.Data
		action_maker: DF.Link | None
		allow_recipient_to_redirect: DF.Check
		amended_from: DF.Link | None
		created_by: DF.Link | None
		details: DF.Text | None
		employee_name: DF.Data | None
		from_company: DF.Link | None
		from_department: DF.Link | None
		from_designation: DF.Link | None
		naming_series: DF.Data | None
		review_transactions: DF.Link
		type: DF.Literal["Redirected", "Approved", "Rejected", "Canceled"]
	# end: auto-generated types
	pass
