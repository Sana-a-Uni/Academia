# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt
import json

import frappe
from frappe.model.document import Document


class SpecificTransactionDocumentAction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from academia.transactions.doctype.transaction_recipients_new.transaction_recipients_new import (
			TransactionRecipientsNew,
		)

		action_date: DF.Data | None
		action_maker: DF.Link | None
		allow_recipient_to_redirect: DF.Check
		amended_from: DF.Link | None
		created_by: DF.Link | None
		details: DF.Text | None
		employee_name: DF.Data | None
		from_company: DF.Link | None
		from_department: DF.Link | None
		from_designation: DF.Link | None
		recipients: DF.Table[TransactionRecipientsNew]
		specific_transaction_document: DF.Link
		type: DF.Literal["Redirected", "Approved", "Rejected", "Canceled"]
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
					doctype="Specific Transaction Document",
					name=self.specific_transaction_document,
					user=recipient.user_id,
					read=1,
					write=1,
					share=1,
					submit=1,
				)


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


@frappe.whitelist()
def update_specific_transaction_document(
	specific_transaction_document_name, current_action_maker, allow_to_redirect, status=""
):
	"""
	Updates the specified fields of an Specific Transaction Document document.

	Args:
		specific_transaction_document_name (str): The name of the Specific Transaction Document document to update.
		current_action_maker (str): The new value for the 'current_action_maker' field.
		allow_to_redirect (int): The new value for the 'allow_to_redirect' checkbox (0 or 1).
		status (str): The new value for the 'status' field.

	Returns:
		dict: Updated document data.
	"""
	if not specific_transaction_document_name:
		frappe.throw(_("Specific Transaction Document name is required"))

	# Fetch the document
	doc = frappe.get_doc("Specific Transaction Document", specific_transaction_document_name)

	# Update fields
	doc.current_action_maker = current_action_maker
	if allow_to_redirect:
		doc.direction = "Downward"
	doc.allow_to_redirect = allow_to_redirect
	if status:
		doc.status = status

	# Save the document
	doc.save()
	frappe.db.commit()  # Commit the changes to the database

	return doc.as_dict()  # Return the updated document as a dictionary
