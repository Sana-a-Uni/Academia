# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import json

import frappe
from frappe.model.document import Document


class InboxMemo(Document):
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
		current_action_maker: DF.Data | None
		external_entity_designation: DF.Link | None
		external_entity_employee: DF.Data | None
		full_electronic: DF.Check
		inbox_from: DF.Literal["Company within the system", "Company outside the system"]
		main_external_entity: DF.Link | None
		recipients: DF.Table[TransactionRecipientsNew]
		start_from: DF.Link
		start_from_company: DF.Link
		start_from_department: DF.Link | None
		start_from_designation: DF.Link | None
		start_from_employee: DF.Data
		status: DF.Literal["Pending", "Completed", "Canceled", "Closed", "Rejected"]
		sub_external_entity: DF.Link | None
		title: DF.Data
	# end: auto-generated types
	pass


@frappe.whitelist()
def create_new_inbox_memo_action(user_id, inbox_memo, type, details):
	"""
	Create a new document in Transaction Action and pass the relevant data from Transaction.
	This function will be called when a button is pressed in Transaction.
	"""
	inbox_memo_doc = frappe.get_doc("Inbox Memo", inbox_memo)

	if inbox_memo_doc.inbox_from == "Company outsite the system":
		pass

	action_maker = inbox_memo_doc.recipients[0]
	if action_maker:
		new_doc = frappe.new_doc("Inbox Memo Action")
		new_doc.inbox_memo = inbox_memo
		new_doc.type = type
		new_doc.from_company = action_maker.recipient_company
		new_doc.from_department = action_maker.recipient_department
		new_doc.from_designation = action_maker.recipient_designation
		new_doc.details = details
		new_doc.action_date = frappe.utils.today()
		new_doc.created_by = action_maker.recipient_email
		new_doc.save(ignore_permissions=True)
		new_doc.submit()

		action_name = new_doc.name

		# check_result = check_all_recipients_action(inbox_memo, user_id)

		# if check_result:
		# 	inbox_memo_doc = frappe.get_doc("Transaction", transaction_name)

		# 	next_step = inbox_memo_doc.step + 1
		# 	next_step_recipients = frappe.get_all(
		# 		"Transaction Recipients",
		# 		filters={"parent": inbox_memo_doc.name, "step": ("=", next_step)},
		# 		fields=["recipient_email", "step"],
		# 	)
		# 	if len(next_step_recipients) > 0:
		# 		for recipient in next_step_recipients:
		# 			frappe.share.add(
		# 				doctype="Transaction",
		# 				name=inbox_memo_doc.name,
		# 				user=recipient.recipient_email,
		# 				read=1,
		# 				write=1,
		# 				share=1,
		# 				submit=1,
		# 			)
		# 		inbox_memo_doc.step = next_step
		# 	else:
		if type == "Approved":
			inbox_memo_doc.status = "Completed"
		elif type == "Rejected":
			inbox_memo_doc.status = "Rejected"

		inbox_memo_doc.complete_time = frappe.utils.now()
		inbox_memo_doc.current_action_maker = ""

		inbox_memo_doc.save(ignore_permissions=True)

		permissions = {"read": 1, "write": 0, "share": 0, "submit": 0}
		permissions_str = json.dumps(permissions)
		update_share_permissions(inbox_memo, user_id, permissions_str)

		return {"message": "Action Success", "action_name": action_name}
	else:
		return {"message": "No employee found for the given user ID."}


@frappe.whitelist()
def update_share_permissions(docname, user, permissions):
	share = frappe.get_all(
		"DocShare",
		filters={"share_doctype": "Inbox Memo", "share_name": docname, "user": user},
	)
	permissions_dict = json.loads(permissions)
	if share:
		# Share entry exists, update the permissions
		share = frappe.get_doc("DocShare", share[0].name)
		share.update(permissions_dict)
		share.save(ignore_permissions=True)
		frappe.db.commit()
		return share
	else:
		return None
