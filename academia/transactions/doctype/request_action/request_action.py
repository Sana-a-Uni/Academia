# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RequestAction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.transactions.doctype.transaction_recipients_new.transaction_recipients_new import (
			TransactionRecipientsNew,
		)
		from frappe.types import DF

		action_date: DF.Date
		action_maker: DF.Link | None
		amended_from: DF.Link | None
		created_by: DF.Data | None
		details: DF.Text | None
		employee_name: DF.ReadOnly | None
		from_company: DF.ReadOnly | None
		from_department: DF.ReadOnly | None
		from_designation: DF.ReadOnly | None
		recipients: DF.Table[TransactionRecipientsNew]
		request: DF.Link
		type: DF.Literal["Redirected", "Approved", "Rejected", "Canceled", "Topic"]

	# end: auto-generated types
	def on_submit(self):

		if len(self.recipients) > 0:
			for row in self.recipients:
				recipient = frappe.get_doc("Employee", row.recipient)
				# if row.applicant_type == "User":
				# 	appicant_user_id = applicant.email
				# else:
				# 	appicant_user_id = applicant.user_id
				frappe.share.add(
					doctype="Request",
					name=self.request,
					user=recipient.user_id,
					read=1,
					write=1,
					share=1,
					submit=1,
				)


@frappe.whitelist()
def get_direct_reports_to_hierarchy_reverse(employee_name):
	employees = []

	# Get employees with reports_to set as the given employee
	direct_reports = frappe.get_all(
		"Employee", filters={"reports_to": employee_name}, fields=["user_id", "name"]
	)

	# Iterate over direct reports
	for employee in direct_reports:
		# frappe.msgprint(f"Direct report found: {employee.user_id}")
		employees.append(employee.user_id)

	return employees
