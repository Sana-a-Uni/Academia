# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Request(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from academia.transactions.doctype.transaction_attachments_new.transaction_attachments_new import (
			TransactionAttachmentsNew,
		)
		from academia.transactions.doctype.transaction_recipients_new.transaction_recipients_new import (
			TransactionRecipientsNew,
		)

		amended_from: DF.Link | None
		attachments: DF.Table[TransactionAttachmentsNew]
		full_electronic: DF.Check
		recipients: DF.Table[TransactionRecipientsNew]
		start_from: DF.Link
		start_from_company: DF.Link | None
		start_from_department: DF.Link | None
		start_from_designation: DF.Link | None
		start_from_employee: DF.Data | None
		status: DF.Literal["Pending", "Completed", "Canceled", "Closed", "Rejected"]
		title: DF.Data
	# end: auto-generated types
	pass


@frappe.whitelist()
def get_reports_to_hierarchy(employee_name):
	reports_emails = []
	employee = frappe.get_doc("Employee", employee_name)
	reports_to = employee.reports_to
	reports_emails.append(reports_to)

	while reports_to:
		employee = frappe.get_doc("Employee", reports_to)
		reports_emails.append(employee.user_id)
		reports_to = employee.reports_to

	return reports_emails
