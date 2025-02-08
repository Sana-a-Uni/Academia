# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt
import json

import frappe
from frappe.model.document import Document


class SpecificTransactionDocument(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.transactions.doctype.recipient_path.recipient_path import RecipientPath
		from academia.transactions.doctype.signatures.signatures import Signatures
		from academia.transactions.doctype.transaction_attachments_new.transaction_attachments_new import TransactionAttachmentsNew
		from academia.transactions.doctype.transaction_recipients_new.transaction_recipients_new import TransactionRecipientsNew
		from frappe.types import DF

		allow_to_redirect: DF.Check
		amended_from: DF.Link | None
		attachments: DF.Table[TransactionAttachmentsNew]
		current_action_maker: DF.Data | None
		direction: DF.Literal["Upward", "Downward"]
		document_content: DF.TextEditor | None
		employee_name: DF.Data | None
		full_electronic: DF.Check
		is_received: DF.Check
		naming_series: DF.Literal["STD-.YY.-.MM.-"]
		recipients: DF.Table[TransactionRecipientsNew]
		recipients_path: DF.Table[RecipientPath]
		signatures: DF.Table[Signatures]
		start_from: DF.Link | None
		start_from_company: DF.Link | None
		start_from_department: DF.Link | None
		start_from_designation: DF.Link | None
		status: DF.Literal["Pending", "Completed", "Canceled", "Closed", "Rejected"]
		template_is_active: DF.Check
		template_name: DF.Link | None
		title: DF.Data | None
		transaction_reference: DF.Link
		type: DF.Literal["\u0643\u0634\u0641", "\u0648\u0631\u0642\u0629"]
		using_path_template: DF.Check
	# end: auto-generated types

	def before_submit(self):
		"""
		Append the reporting chain to the 'Signatures' child table in the current document.

		Include only the employees between the start employee and end employee in the chain.
		"""

		reporting_chain = []
		visited = set()
		if not self.using_path_template and len(self.recipients) > 0:
			current_employee = self.start_from  # Fieldname for the starting employee
			end_employee = self.recipients[0].recipient  # Fieldname for the target employee

			# Append the reporting chain to the 'Signatures' child table
			for emp in reporting_chain:
				self.append("signatures", {
					"employee_name": emp["employee_name"],
					"employee_designation": emp["employee_designation"]
				})
			
		elif self.using_path_template and len(self.recipients_path) > 0:
			current_employee = self.start_from  # Fieldname for the starting employee
			end_employee = self.recipients_path[-1].recipient

			# Append the reporting chain to the 'Signatures' child table
			for path in self.recipients_path:
				self.append("signatures", {
					"employee_name": path.recipient_company,
					"employee_designation": path.recipient_department
				})


		# We need to start from the employee who directly reports to the current_employee
		employee_doc = frappe.get_doc("Employee", current_employee)
		employee_to_process = employee_doc.reports_to

		# Traverse the reporting chain until we reach the end employee
		while employee_to_process:
			if employee_to_process in visited:
				frappe.throw("Circular reporting chain detected.")
			visited.add(employee_to_process)

			# Fetch the employee's document
			employee_doc = frappe.get_doc("Employee", employee_to_process)
			reports_to = employee_doc.reports_to

			# Break if we reach the end employee
			if employee_to_process == end_employee or not reports_to:
				break
			
			# Append intermediate employees (skip current_employee and end_employee)
			if reports_to != current_employee:
				reporting_chain.append({
					"employee": reports_to,
					"employee_name": f"{employee_doc.first_name} {employee_doc.last_name or ''}".strip(),
					"employee_designation": employee_doc.designation
				})

			# Move to the next employee in the chain
			employee_to_process = reports_to


	def on_submit(self):
		
		employee = frappe.get_doc("Employee", self.start_from)
		frappe.share.add(
			doctype="Specific Transaction Document",
			name=self.name,
			user=employee.user_id,
			read=1,
			write=0,
			share=0,
		)

		if self.start_from and not self.using_path_template:
			employee = frappe.get_doc("Employee", self.start_from, fields=["reports_to", "user_id"])
			share_permission_through_route(self, employee)

		elif self.template_name:
			frappe.share.add(
				doctype="Specific Transaction Document",
				name=self.name,
				user=self.recipients_path[0].recipient_email,
				read=1,
				write=1,
				share=1,
				submit=1,
			)

		# make a read permission for applicants
		# for row in self.recipients:
		# 	recipient = frappe.get_doc("Employee", row.recipient)
		# 	# if row.applicant_type == "User":
		# 	# 	appicant_user_id = applicant.email
		# 	# else:
		# 	# 	appicant_user_id = applicant.user_id
		# 	frappe.share.add(
		# 		doctype="Specific Transaction Document",
		# 		name=self.name,
		# 		user=recipient.user_id,
		# 		read=1,
		# 	)

		# if self.through_route == 1:
		# 	employee = frappe.get_doc("Employee", self.start_with, fields=["reports_to", "user_id"])
		# 	share_permission_through_route(self, employee)

		# elif self.transaction_scope == "Among Companies":
		# 	company_head = frappe.get_doc("Transaction Company Head", {"company": self.start_with_company})
		# 	head_employee_id = company_head.head_employee
		# 	employee_user = frappe.get_doc("Employee", head_employee_id)
		# 	user_id = employee_user.user_id
		# 	recipients = [
		# 		{
		# 			"step": 1,
		# 			"recipient_name": employee_user.employee_name,
		# 			"recipient_company": employee_user.company,
		# 			"recipient_department": employee_user.department,
		# 			"recipient_designation": employee_user.designation,
		# 			"recipient_email": user_id,
		# 			"has_sign": 0,
		# 			"print_paper": 0,
		# 			"is_received": 0,
		# 		}
		# 	]
		# 	create_redirect_action(self.owner, self.name, recipients, self.step, 1)

		# 	frappe.share.add(
		# 		doctype="Transaction",
		# 		name=self.name,
		# 		user=user_id,
		# 		read=1,
		# 		write=1,
		# 		share=1,
		# 		submit=1,
		# 	)
		# 	frappe.db.commit()
		# else:
		# 	create_redirect_action(self.owner, self.name, self.recipients, self.step, 1)
		# 	# make a read, write, share permissions for reciepents
		# 	for row in self.recipients:
		# 		if row.step == 1:
		# 			frappe.share.add(
		# 				doctype="Transaction",
		# 				name=self.name,
		# 				user=row.recipient_email,
		# 				read=1,
		# 				write=1,
		# 				share=1,
		# 				submit=1,
		# 			)
		# 	frappe.db.commit()

		###########################


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
def create_new_specific_transaction_document_action(user_id, specific_transaction_document, type, details,created_by):
	"""
	Create a new document in Transaction Action and pass the relevant data from Transaction.
	This function will be called when a button is pressed in Transaction.
	"""
	specific_transaction_document_doc = frappe.get_doc(
		"Specific Transaction Document", specific_transaction_document
	)  # Fetch the specific_transaction_document as a document
	action_maker = frappe.get_doc("Employee", {"user_id": user_id})

	recipients = []
	reports_to_emp = None  # Initialize the reports_to_emp variable as None

	# Ensure the recipients child table is accessed correctly
	if (
		len(specific_transaction_document_doc.recipients) > 0
		and action_maker.user_id != specific_transaction_document_doc.recipients[0].recipient_email
		and type == "Approved"
		and specific_transaction_document_doc.using_path_template == False
	):  # Access the recipients attribute on the document
		if specific_transaction_document_doc.direction == "Upward":
			reports_to = action_maker.reports_to
			reports_to_emp = frappe.get_doc("Employee", reports_to)
			if type != "Rejected":
				frappe.share.add(
					doctype="Transaction New", 
					name=specific_transaction_document_doc.transaction_reference, 
					user=reports_to_emp.user_id, 
					read=1, 
					write=1, 
					share=1, 
					submit=1
				)
				frappe.share.add(
					doctype="Specific Transaction Document",
					name=specific_transaction_document_doc.name,
					user=reports_to_emp.user_id,
					read=1,
					write=1,
					share=1,
					submit=1,
				)
			recipient = {
				"step": 1,
				"recipient": reports_to_emp.name,
				"recipient_name": reports_to_emp.employee_name,
				"recipient_company": reports_to_emp.company,
				"recipient_department": reports_to_emp.department,
				"recipient_designation": reports_to_emp.designation,
				"recipient_email": reports_to_emp.user_id,
			}
			recipients = [recipient]
		else:
			specific_transaction_document_doc.status = "Completed"
			specific_transaction_document_doc.complete_time = frappe.utils.now()
			specific_transaction_document_doc.current_action_maker = ""

			specific_transaction_document_doc.save(ignore_permissions=True)
			permissions = {"read": 1, "write": 0, "share": 0, "submit": 0}
			permissions_str = json.dumps(permissions)
			update_share_permissions(specific_transaction_document, user_id, permissions_str)
			
	elif specific_transaction_document_doc.using_path_template:
		if action_maker.user_id == specific_transaction_document_doc.recipients_path[-1].recipient_email:
			if type == "Approved":
				specific_transaction_document_doc.status = "Completed"
			elif type == "Rejected":
				specific_transaction_document_doc.status = "Rejected"
			specific_transaction_document_doc.complete_time = frappe.utils.now()
			specific_transaction_document_doc.current_action_maker = ""
			specific_transaction_document_doc.save(ignore_permissions=True)
		else:
			for i, recipient in enumerate(specific_transaction_document_doc.recipients_path):
				if recipient.recipient_email == action_maker.user_id:
					next_recipient_email = specific_transaction_document_doc.recipients_path[i + 1].recipient_email if i < len(specific_transaction_document_doc.recipients_path) else None
					specific_transaction_document_doc.current_action_maker = next_recipient_email
					specific_transaction_document_doc.save(ignore_permissions=True)
					permissions = {"read": 1, "write": 1, "share": 1, "submit": 1}
					permissions_str = json.dumps(permissions)
					frappe.share.add(
						doctype="Specific Transaction Document", 
						name=specific_transaction_document_doc.name, 
						user=next_recipient_email, 
						read=1, 
						write=1, 
						share=1, 
						submit=1
					)
					frappe.share.add(
						doctype="Transaction New", 
						name=specific_transaction_document_doc.transaction_reference, 
						user=next_recipient_email, 
						read=1, 
						write=1, 
						share=1, 
						submit=1
					)
					break
	elif type == "Rejected":
		specific_transaction_document_doc.status = "Rejected"

		specific_transaction_document_doc.complete_time = frappe.utils.now()
		specific_transaction_document_doc.current_action_maker = ""
		specific_transaction_document_doc.save(ignore_permissions=True)
		permissions = {"read": 1, "write": 0, "share": 0, "submit": 0}
		permissions_str = json.dumps(permissions)
		update_share_permissions(specific_transaction_document, user_id, permissions_str)

	else:
		if (
			(action_maker.user_id == specific_transaction_document_doc.recipients[0].recipient_email or specific_transaction_document_doc.recipients_path[-1].recipient_email == action_maker.user_id)
			and type == "Approved"
		):
			specific_transaction_document_doc.status = "Completed"
		elif type == "Rejected":
			specific_transaction_document_doc.status = "Rejected"

		specific_transaction_document_doc.complete_time = frappe.utils.now()
		specific_transaction_document_doc.current_action_maker = ""

		specific_transaction_document_doc.save(ignore_permissions=True)
		permissions = {"read": 1, "write": 0, "share": 0, "submit": 0}
		permissions_str = json.dumps(permissions)
		update_share_permissions(specific_transaction_document, user_id, permissions_str)

		# Ensure action_maker is properly defined
	if action_maker:
		new_doc = frappe.new_doc("Specific Transaction Document Action")
		new_doc.specific_transaction_document = specific_transaction_document
		new_doc.type = type
		new_doc.action_maker = action_maker.name
		new_doc.from_company = action_maker.company
		new_doc.from_department = action_maker.department
		new_doc.from_designation = action_maker.designation
		new_doc.details = details
		new_doc.action_date = frappe.utils.today()
		new_doc.created_by = created_by  # Use user_id instead of recipient_email
		new_doc.naming_series = specific_transaction_document + "-ACT-"


		# Ensure recipients is properly defined
		if recipients:
			for recipient in recipients:
				new_doc.append(
					"recipients",
					{
						"step": recipient.get("step"),
						"recipient": recipient.get("recipient"),
						"recipient_name": recipient.get("recipient_name"),
						"recipient_company": recipient.get("recipient_company"),
						"recipient_department": recipient.get("recipient_department"),
						"recipient_designation": recipient.get("recipient_designation"),
						"recipient_email": recipient.get("recipient_email"),
					},
				)

		new_doc.insert(ignore_permissions=True)
		frappe.db.commit()
		new_doc.save()
		new_doc.submit()

		action_name = new_doc.name
		if reports_to_emp:
			return {
				"message": "Action Success",
				"action_name": action_name,
				"action_maker": reports_to_emp.user_id or "",
			}
		elif specific_transaction_document_doc.using_path_template:
			for i, recipient in enumerate(specific_transaction_document_doc.recipients_path):
				if recipient.recipient_email == action_maker.user_id:
					if i + 1 < len(specific_transaction_document_doc.recipients_path):
						next_recipient_email = specific_transaction_document_doc.recipients_path[i + 1].recipient_email
					else:
						next_recipient_email = None
					break
			if next_recipient_email:
				return {
					"message": "Action Success",
					"action_name": action_name,
					"action_maker": next_recipient_email or "",
				}
			else:
				return {
					"message": "Action Success",
					"action_name": action_name,
					"action_maker": "",
				}
		else:
			return {"message": "Action Success", "action_name": action_name, "action_maker": ""}
	else:
		return {"message": "No employee found for the given user ID."}


@frappe.whitelist()
def update_share_permissions(docname, user, permissions):
	share = frappe.get_all(
		"DocShare",
		filters={"share_doctype": "Specific Transaction Document", "share_name": docname, "user": user},
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


def share_permission_through_route(document, current_employee):
	reports_to = current_employee.reports_to
	if current_employee.user_id != document.recipients[0].recipient_email:
		reports_to_emp = frappe.get_doc("Employee", reports_to)
		# if reports_to_emp != document.recipients[0].recipient_email:
		frappe.share.add(
			doctype="Specific Transaction Document",
			name=document.name,
			user=reports_to_emp.user_id,
			read=1,
			write=1,
			share=1,
			submit=1,
		)


@frappe.whitelist()
def get_specific_transaction_document_actions_html(specific_transaction_document_name):
	actions = frappe.get_all(
		"Specific Transaction Document Action",
		filters={"specific_transaction_document": specific_transaction_document_name, "docstatus": 1},
		fields=["name", "type", "action_date", "action_maker", "details"],
		order_by="creation asc",
	)

	if not actions:
		return "<p>No actions found for this specific transaction document.</p>"

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
            <td><a href="/app/specific_transaction_document-action/{action['name']}" target="_blank">{action['name']}</a></td>
            <td style="color: white; background-color: {type_color}; padding: 5px; border-radius: 10px; text-align: center; width: 100%;">{action['type']}</td>
            <td>{action['action_date']}</td>
            <td>{action['action_maker']}</td>
            <td>{action['details'] or ''}</td>
        </tr>
        """
	table_html += "</tbody></table>"

	return table_html


@frappe.whitelist()
def get_shared_std(user):
    shared_std = frappe.get_all('DocShare', filters={'user': user, 'share_doctype': 'Specific Transaction Document'}, fields=['share_name'])
    std_names = [memo['share_name'] for memo in shared_std]
    return shared_std

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