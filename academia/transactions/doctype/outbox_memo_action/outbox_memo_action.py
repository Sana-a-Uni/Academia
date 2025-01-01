# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class OutboxMemoAction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.transactions.doctype.transaction_recipients_new.transaction_recipients_new import TransactionRecipientsNew
		from frappe.types import DF

		action_date: DF.Data
		action_maker: DF.Link | None
		allow_recipient_to_redirect: DF.Check
		amended_from: DF.Link | None
		created_by: DF.Link | None
		details: DF.Text | None
		employee_name: DF.Data | None
		from_company: DF.Data | None
		from_department: DF.Data | None
		from_designation: DF.Data | None
		outbox_memo: DF.Link
		recipients: DF.Table[TransactionRecipientsNew]
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
				if self.allow_recipient_to_redirect:
					frappe.share.add(
						doctype="Outbox Memo",
						name=self.outbox_memo,
						user=recipient.user_id,
						read=1,
						write=1,
						share=1,
						submit=1,
					)
				else:
					frappe.share.add(
						doctype="Outbox Memo",
						name=self.outbox_memo,
						user=recipient.user_id,
						read=1,
						write=0,
						share=0,
						submit=0,
					)



import frappe


@frappe.whitelist()
def update_outbox_memo(outbox_memo_name, current_action_maker, allow_to_redirect, status=""):
	"""
	Updates the specified fields of an Outbox Memo document.

	Args:
		outbox_memo_name (str): The name of the Outbox Memo document to update.
		current_action_maker (str): The new value for the 'current_action_maker' field.
		allow_to_redirect (int): The new value for the 'allow_to_redirect' checkbox (0 or 1).
		status (str): The new value for the 'status' field.

	Returns:
		dict: Updated document data.
	"""
	if not outbox_memo_name:
		frappe.throw("Outbox Memo name is required")

	# Fetch the document
	doc = frappe.get_doc("Outbox Memo", outbox_memo_name)

	# Update fields
	doc.current_action_maker = current_action_maker
	doc.allow_to_redirect = allow_to_redirect
	if status:
		doc.status = status
	# Save the document
	doc.save()
	frappe.db.commit()  # Commit the changes to the database

	return doc.as_dict()  # Return the updated document as a dictionary
