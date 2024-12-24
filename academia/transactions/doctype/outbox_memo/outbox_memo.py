# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class OutboxMemo(Document):
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
		direction: DF.Literal["", "Upward", "Downward"]
		full_electronic: DF.Check
		recipients: DF.Table[TransactionRecipientsNew]
		start_from: DF.Link
		start_from_company: DF.Link
		start_from_department: DF.Link | None
		start_from_designation: DF.Link | None
		start_from_employee: DF.Data
		status: DF.Literal["Pending", "Completed", "Canceled", "Closed", "Rejected"]
		title: DF.Data
		type: DF.Literal["Internal", "External"]
	# end: auto-generated types
	pass


@frappe.whitelist()
def get_all_employees_except_start_from_company(start_from_company):
	employees = frappe.get_list(
		"Employee", filters={"company": ["!=", start_from_company]}, fields=["user_id"]
	)
	return [emp.user_id for emp in employees]


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


@frappe.whitelist()
def get_reports_to_hierarchy_reverse(employee_name):
	employees = []

	# Get employees with reports_to set as the given employee
	direct_reports = frappe.get_all(
		"Employee", filters={"reports_to": employee_name}, fields=["user_id", "name"]
	)

	# Iterate over direct reports
	for employee in direct_reports:
		# frappe.msgprint(f"{employee.user_id}")
		employees.append(employee.user_id)

		# Recursively call the function for each direct report
		employees += get_reports_to_hierarchy_reverse(employee.name)

	return employees
