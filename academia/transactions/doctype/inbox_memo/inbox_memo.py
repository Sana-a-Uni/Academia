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
		from academia.transactions.doctype.transaction_attachments_new.transaction_attachments_new import TransactionAttachmentsNew
		from academia.transactions.doctype.transaction_recipients_new.transaction_recipients_new import TransactionRecipientsNew
		from frappe.types import DF

		amended_from: DF.Link | None
		attachments: DF.Table[TransactionAttachmentsNew]
		current_action_maker: DF.Data | None
		document_content: DF.TextEditor | None
		external_entity_designation: DF.Data | None
		external_entity_employee: DF.Data | None
		full_electronic: DF.Check
		inbox_from: DF.Literal["Company within the system", "Company outside the system"]
		is_received: DF.Check
		main_external_entity: DF.Link | None
		naming_series: DF.Literal["INBOX-.YY.-.MM.-"]
		recipients: DF.Table[TransactionRecipientsNew]
		start_from: DF.Link | None
		start_from_company: DF.Link | None
		start_from_department: DF.Link | None
		start_from_designation: DF.Link | None
		start_from_employee: DF.Data | None
		status: DF.Literal["Pending", "Completed", "Canceled", "Closed", "Rejected"]
		sub_external_entity: DF.Link | None
		title: DF.Data
		transaction_reference: DF.Link | None
	# end: auto-generated types
	def on_submit(self):
		if self.inbox_from == "Company within the system":
			employee = frappe.get_doc("Employee", self.start_from)
			frappe.share.add(
				doctype="inbox Memo",
				name=self.name,
				user=employee.user_id,
				read=1,
				write=0,
				share=0,
			)

		employee = frappe.get_doc("Employee", self.recipients[0].recipient)
		frappe.share.add(
			doctype="inbox Memo",
			name=self.name,
			user=employee.user_id,
			read=1,
			write=1,
			share=1,
			submit=1,
		)

@frappe.whitelist()
def create_new_inbox_memo_action(user_id, inbox_memo, type, details):
	"""
	Create a new document in Transaction Action and pass the relevant data from Transaction.
	This function will be called when a button is pressed in Transaction.
	"""
	inbox_memo_doc = frappe.get_doc("Inbox Memo", inbox_memo)

	if inbox_memo_doc.inbox_from == "Company outsite the system":
		pass

	action_maker = frappe.get_doc("Employee", {"user_id": user_id})
	if action_maker:
		new_doc = frappe.new_doc("Inbox Memo Action")
		new_doc.inbox_memo = inbox_memo
		new_doc.type = type
		new_doc.from_company = action_maker.company
		new_doc.from_department = action_maker.department
		new_doc.from_designation = action_maker.designation
		new_doc.action_maker = action_maker.user_id
		new_doc.details = details
		new_doc.action_date = frappe.utils.today()
		new_doc.created_by = action_maker.user_id
		new_doc.naming_series = inbox_memo + "-ACT-"
		new_doc.save(ignore_permissions=True)
		new_doc.submit()

		action_name = new_doc.name

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
def get_all_employees_except_start_with_company(start_with_company):
	employees = frappe.get_list(
		"Employee", filters={"company": ["!=", start_with_company]}, fields=["user_id"]
	)
	return [emp.user_id for emp in employees]


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
		return "text"


@frappe.whitelist()
def get_request_actions_html(inbox_memo_name):
	actions = frappe.get_all(
		"Inbox Memo Action",
		filters={"inbox_memo": inbox_memo_name, "docstatus": 1},
		fields=["name", "type", "action_date", "action_maker", "details"],
		order_by="creation asc",
	)

	if not actions:
		return "<p>No actions found for this Inbox Memo.</p>"

	table_html = """
    <table class="table table-bordered" style="table-layout: fixed; width: 100%; word-wrap: break-word;">
        <thead>
            <tr>
                <th style="width: 20%;">Action Name</th>
                <th style="width: 15%;">Type</th>
                <th style="width: 15%;">Action Date</th>
                <th style="width: 20%;">Action Maker</th>
                <th style="width: 30%;">Details</th>
            </tr>
        </thead>
        <tbody>
    """

	type_colors = {
		"Pending": "gray",
		"Redirected": "blue",
		"Approved": "green",
		"Rejected": "red",
		"Canceled": "orange",
		"Topic": "purple",
	}

	for action in actions:
		type_color = type_colors.get(action["type"], "black")
		action_maker = action["action_maker"] if action["action_maker"] else "None"

		table_html += f"""
        <tr>
            <td><a href="/app/inbox-memo-action/{action['name']}" target="_blank">{action['name']}</a></td>
            <td style="color: white; background-color: {type_color}; padding: 5px; border-radius: 10px; text-align: center; width: 100%;">{action['type']}</td>
            <td>{action['action_date']}</td>
            <td>{action['action_maker']}</td>
            <td>{action['details'] or ''}</td>
        </tr>
        """
	table_html += "</tbody></table>"

	return table_html
