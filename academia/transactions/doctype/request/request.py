# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt
import json
import frappe
import os
from jinja2 import Template
from frappe.model.document import Document


class Request(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.transactions.doctype.recipient_path.recipient_path import RecipientPath
		from academia.transactions.doctype.transaction_attachments_new.transaction_attachments_new import TransactionAttachmentsNew
		from academia.transactions.doctype.transaction_recipients_new.transaction_recipients_new import TransactionRecipientsNew
		from frappe.types import DF

		amended_from: DF.Link | None
		attachments: DF.Table[TransactionAttachmentsNew]
		current_action_maker: DF.Data | None
		document_content: DF.TextEditor | None
		full_electronic: DF.Check
		is_received: DF.Check
		naming_series: DF.Literal["REQ-.YY.-.MM.-"]
		recipients: DF.Table[TransactionRecipientsNew]
		recipients_path: DF.Table[RecipientPath]
		start_from: DF.Link
		start_from_company: DF.Link | None
		start_from_department: DF.Link | None
		start_from_designation: DF.Link | None
		start_from_employee: DF.Data | None
		status: DF.Literal["Pending", "Completed", "Canceled", "Closed", "Rejected"]
		template_is_active: DF.Check
		template_name: DF.Link | None
		title: DF.Data
		transaction_reference: DF.Link | None
		using_path_template: DF.Check
	# end: auto-generated types
	
	def on_submit(self):
		employee = frappe.get_doc("Employee", self.start_from)
		frappe.share.add(
			doctype="Request",
			name=self.name,
			user=employee.user_id,
			read=1,
			write=0,
			share=0,
		)

		if not self.using_path_template:
			frappe.share.add(
					doctype="Request",
					name=self.name,
					user=self.recipients[0].recipient_email,
					read=1,
					write=1,
					share=1,
					submit=1,
				)


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
def create_new_request_action(user_id, request, type, details, created_by):
	"""
	Create a new document in Transaction Action and pass the relevant data from Transaction.
	This function will be called when a button is pressed in Transaction.
	"""
	request_doc = frappe.get_doc("Request", request)

	action_maker = frappe.get_doc("Employee", {"user_id": user_id})
	if action_maker:
		new_doc = frappe.new_doc("Request Action")
		new_doc.request = request
		new_doc.type = type
		new_doc.from_company = action_maker.company
		new_doc.from_department = action_maker.department
		new_doc.from_designation = action_maker.designation
		new_doc.action_maker = action_maker.user_id
		new_doc.details = details
		new_doc.action_date = frappe.utils.today()
		new_doc.created_by = created_by
		new_doc.naming_series = request + "-ACT-"
		new_doc.save(ignore_permissions=True)
		new_doc.submit()

		action_name = new_doc.name

		if type == "Approved":
			if request_doc.using_path_template and request_doc.template_is_active:
				if action_maker.user_id == request_doc.recipients_path[-1].recipient_email:
					request_doc.status = "Completed"
					request_doc.complete_time = frappe.utils.now()
					request_doc.current_action_maker = ""
				else:
					for i, recipient in enumerate(request_doc.recipients_path):
						if recipient.recipient_email == action_maker.user_id:
							next_recipient_email = request_doc.recipients_path[i + 1].recipient_email if i < len(request_doc.recipients_path) else None
							request_doc.current_action_maker = next_recipient_email

							#update the transaction_holder
							transaction_doc = frappe.get_doc("Transaction New", request_doc.transaction_reference)
							transaction_doc.transaction_holder = next_recipient_email
							transaction_doc.save(ignore_permissions=True)
							
							permissions = {"read": 1, "write": 1, "share": 1, "submit": 1}
							permissions_str = json.dumps(permissions)
							update_share_permissions(request, next_recipient_email, permissions_str)
							break
			
			elif not request_doc.using_path_template or not request_doc.template_is_active:
				request_doc.status = "Completed"
				request_doc.complete_time = frappe.utils.now()
				request_doc.current_action_maker = ""

		elif type == "Rejected":
			request_doc.status = "Rejected"
			request_doc.complete_time = frappe.utils.now()
			request_doc.current_action_maker = ""

		request_doc.save(ignore_permissions=True)

		permissions = {"read": 1, "write": 0, "share": 0, "submit": 0}
		permissions_str = json.dumps(permissions)
		update_share_permissions(request, user_id, permissions_str)

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
		filters={"share_doctype": "Request", "share_name": docname, "user": user},
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
def get_shared_requests(user):
    shared_memos = frappe.get_all('DocShare', filters={'user': user, 'share_doctype': 'Request'}, fields=['share_name'])
    memo_names = [memo['share_name'] for memo in shared_memos]
    return memo_names

@frappe.whitelist()
def get_request_actions_html(request_name):
	actions = frappe.get_all(
		"Request Action",
		filters={"request": request_name, "docstatus": 1},
		fields=["name", "type", "action_date", "created_by", "details"],
		order_by="creation asc",
	)

	if not actions:
		return "<p>No actions found for this request.</p>"

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

		table_html += f"""
        <tr>
            <td><a href="/app/request-action/{action['name']}" target="_blank">{action['name']}</a></td>
            <td>{action['type']}</td>
            <td>{action['action_date']}</td>
            <td>{action['created_by']}</td>
            <td>{action['details'] or ''}</td>
        </tr>
        """
	table_html += "</tbody></table>"

	return table_html

@frappe.whitelist()
def copy_template_paths(template_docname):
    # Fetch the template document
    template_doc = frappe.get_doc("Transaction Path Template", template_docname)

    # Prepare data for recipients_path
    recipients_paths = []
    for path in template_doc.template_path:
        recipients_paths.append({
            'doctype': 'Recipients Path',
			'step': path.step,
			'recipient_company': path.recipient_company,
			'recipient_department': path.recipient_department,
			'recipient_designation': path.recipient_designation,
        })

    return recipients_paths