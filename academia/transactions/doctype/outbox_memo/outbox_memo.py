# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import json

import frappe
from frappe.model.document import Document


class OutboxMemo(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.transactions.doctype.transaction_attachments_new.transaction_attachments_new import TransactionAttachmentsNew
		from academia.transactions.doctype.transaction_recipients_new.transaction_recipients_new import TransactionRecipientsNew
		from frappe.types import DF

		allow_to_redirect: DF.Check
		amended_from: DF.Link | None
		attachments: DF.Table[TransactionAttachmentsNew]
		current_action_maker: DF.Data | None
		direction: DF.Literal["Upward", "Downward"]
		document_content: DF.TextEditor | None
		end_employee: DF.Link | None
		end_employee_company: DF.Link | None
		end_employee_department: DF.Link | None
		end_employee_designation: DF.Link | None
		end_employee_name: DF.Data | None
		full_electronic: DF.Check
		recipients: DF.Table[TransactionRecipientsNew]
		start_from: DF.Link
		start_from_company: DF.Link
		start_from_department: DF.Link | None
		start_from_designation: DF.Link | None
		start_from_employee: DF.Data
		status: DF.Literal["Pending", "Completed", "Canceled", "Closed", "Rejected"]
		title: DF.Data
		transaction_reference: DF.Link | None
		type: DF.Literal["Internal", "External"]
	# end: auto-generated types
	def on_submit(self):
		employee = frappe.get_doc("Employee", self.start_from)
		frappe.share.add(
			doctype="Outbox Memo",
			name=self.name,
			user=employee.user_id,
			read=1,
			write=0,
			share=0,
		)

		if self.start_from and self.direction == "Upward":
			employee = frappe.get_doc("Employee", self.start_from, fields=["reports_to", "user_id"])
			share_permission_through_route(self, employee)
			
		elif self.start_from and self.direction == "Downward":
			frappe.share.add(
				doctype="Outbox Memo",
				name=self.name,
				user=self.recipients[0].recipient_email,
				read=1,
				write=1,
				share=1,
				submit=1,
			)


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


@frappe.whitelist()
def get_direct_reports_to_hierarchy_reverse(employee_name):
	employees = []

	# Get employees with reports_to set as the given employee
	direct_reports = frappe.get_all(
		"Employee", filters={"reports_to": employee_name}, fields=["user_id", "name"]
	)

	# Iterate over direct reports
	for employee in direct_reports:
		# frappe.msgprint(f"{employee.user_id}")
		employees.append(employee.user_id)

	return employees


# @frappe.whitelist()
# def create_new_outbox_memo_action(user_id, outbox_memo, type, details):
# 	"""
# 	Create a new document in Transaction Action and pass the relevant data from Transaction.
# 	This function will be called when a button is pressed in Transaction.
# 	"""
# 	outbox_memo_doc = frappe.get_doc("Outbox Memo", outbox_memo)  # Fetch the outbox_memo as a document
# 	action_maker = frappe.get_doc("Employee", {"user_id": user_id})

# 	# if outbox_memo_doc.type == "Internal" & outbox_memo_doc.direction != "Downward":
# 	# 	share_permission_through_route(outbox_memo_doc, action_maker)

# 	if action_maker.user_id != outbox_memo.recipients[0].recipient_email:
# 		reports_to = action_maker.reports_to
# 		reports_to_emp = frappe.get_doc("Employee", reports_to)
# 		frappe.share.add(
# 			doctype="Outbox Memo",
# 			name=outbox_memo_doc.name,
# 			user=reports_to_emp.user_id,
# 			read=1,
# 			write=1,
# 			share=1,
# 			submit=1,
# 		)
# 		# recipient = {
# 		# 	"step": 1,
# 		# 	"recipient_name": reports_to_emp.employee_name,
# 		# 	"recipient_company": reports_to_emp.company,
# 		# 	"recipient_department": reports_to_emp.department,
# 		# 	"recipient_designation": reports_to_emp.designation,
# 		# 	"recipient_email": reports_to_emp.user_id,
# 		# }
# 		# recipients = [recipient]

# 	if action_maker:
# 		new_doc = frappe.new_doc("Outbox Memo Action")
# 		new_doc.outbox_memo = outbox_memo
# 		new_doc.type = type
# 		new_doc.from_company = action_maker.company
# 		new_doc.from_department = action_maker.department
# 		new_doc.from_designation = action_maker.designation
# 		new_doc.details = details
# 		new_doc.action_date = frappe.utils.today()
# 		new_doc.created_by = action_maker.user_id
# 		# if recipients:
# 		# 	for recipient in recipients:
# 		# 		recipients_field = new_doc.append("recipients", {})
# 		# 		recipients_field.step = recipient.get("step")
# 		# 		recipients_field.recipient_name = recipient.get("recipient_name")
# 		# 		recipients_field.recipient_company = recipient.get("recipient_company")
# 		# 		recipients_field.recipient_department = recipient.get("recipient_department")
# 		# 		recipients_field.recipient_designation = recipient.get("recipient_designation")
# 		# 		recipients_field.recipient_email = recipient.get("recipient_email")
# 		new_doc.save(ignore_permissions=True)
# 		new_doc.submit()

# 		action_name = new_doc.name

# 		# check_result = check_all_recipients_action(inbox_memo, user_id)

# 		# if check_result:
# 		# 	inbox_memo_doc = frappe.get_doc("Transaction", transaction_name)

# 		# 	next_step = inbox_memo_doc.step + 1
# 		# 	next_step_recipients = frappe.get_all(
# 		# 		"Transaction Recipients",
# 		# 		filters={"parent": inbox_memo_doc.name, "step": ("=", next_step)},
# 		# 		fields=["recipient_email", "step"],
# 		# 	)
# 		# 	if len(next_step_recipients) > 0:
# 		# 		for recipient in next_step_recipients:
# 		# 			frappe.share.add(
# 		# 				doctype="Transaction",
# 		# 				name=inbox_memo_doc.name,
# 		# 				user=recipient.recipient_email,
# 		# 				read=1,
# 		# 				write=1,
# 		# 				share=1,
# 		# 				submit=1,
# 		# 			)
# 		# 		inbox_memo_doc.step = next_step
# 		# 	else:

# 		if action_maker.user_id == outbox_memo.recipients[0].recipient_email:

# 			if action_maker.user_id == outbox_memo.recipients[0].recipient_email & type == "Approved":
# 				outbox_memo_doc.status = "Completed"
# 			elif type == "Rejected":
# 				outbox_memo_doc.status = "Rejected"

# 			outbox_memo_doc.complete_time = frappe.utils.now()
# 			outbox_memo_doc.current_action_maker = ""

# 			outbox_memo_doc.save(ignore_permissions=True)

# 			permissions = {"read": 1, "write": 0, "share": 0, "submit": 0}
# 			permissions_str = json.dumps(permissions)
# 			update_share_permissions(outbox_memo, user_id, permissions_str)

# 		return {"message": "Action Success", "action_name": action_name}
# 	else:
# 		return {"message": "No employee found for the given user ID."}


@frappe.whitelist()
def create_new_outbox_memo_action(user_id, outbox_memo, type, details):
	"""
	Create a new document in Transaction Action and pass the relevant data from Transaction.
	This function will be called when a button is pressed in Transaction.
	"""
	outbox_memo_doc = frappe.get_doc("Outbox Memo", outbox_memo)  # Fetch the outbox_memo as a document
	action_maker = frappe.get_doc("Employee", {"user_id": user_id})
	if outbox_memo_doc.end_employee:
		end_employee_email = frappe.get_value("Employee", {"name": outbox_memo_doc.end_employee}, "user_id")

	recipients = []
	reports_to_emp = None  # Initialize the reports_to_emp variable as None

	# Ensure the recipients child table is accessed correctly
	if (
		(outbox_memo_doc.type == "Internal" and (action_maker.user_id != outbox_memo_doc.recipients[0].recipient_email and type == "Approved" and outbox_memo_doc.direction != "Downward"))
		or (outbox_memo_doc.type == "External" and (action_maker.user_id != end_employee_email and type == "Approved"))
	):  # Access the recipients attribute on the document
		reports_to = action_maker.reports_to
		reports_to_emp = frappe.get_doc("Employee", reports_to)
		if type != "Rejected":
			frappe.share.add(
				doctype="Outbox Memo",
				name=outbox_memo_doc.name,
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
	elif type == "Approved" and outbox_memo_doc.direction =="Downward":
		outbox_memo_doc.status = "Completed"
		outbox_memo_doc.complete_time = frappe.utils.now()
		outbox_memo_doc.current_action_maker = ""

		outbox_memo_doc.save(ignore_permissions=True)
		permissions = {"read": 1, "write": 0, "share": 0, "submit": 0}
		permissions_str = json.dumps(permissions)
		update_share_permissions(outbox_memo, user_id, permissions_str)
	elif type == "Rejected":
		outbox_memo_doc.status = "Rejected"

		outbox_memo_doc.complete_time = frappe.utils.now()
		outbox_memo_doc.current_action_maker = ""
		outbox_memo_doc.save(ignore_permissions=True)
		permissions = {"read": 1, "write": 0, "share": 0, "submit": 0}
		permissions_str = json.dumps(permissions)
		update_share_permissions(outbox_memo, user_id, permissions_str)

	else:
		if (action_maker.user_id == outbox_memo_doc.recipients[0].recipient_email and type == "Approved") or (outbox_memo_doc.type == "External" and action_maker.user_id == end_employee_email and type == "Approved"):
			outbox_memo_doc.status = "Completed"
		elif type == "Rejected":
			outbox_memo_doc.status = "Rejected"

		outbox_memo_doc.complete_time = frappe.utils.now()
		outbox_memo_doc.current_action_maker = ""

		outbox_memo_doc.save(ignore_permissions=True)
		permissions = {"read": 1, "write": 0, "share": 0, "submit": 0}
		permissions_str = json.dumps(permissions)
		update_share_permissions(outbox_memo, user_id, permissions_str)

		# Ensure action_maker is properly defined
	if action_maker:
		new_doc = frappe.new_doc("Outbox Memo Action")
		new_doc.outbox_memo = outbox_memo
		new_doc.type = type
		new_doc.action_maker = action_maker.name
		new_doc.from_company = action_maker.company
		new_doc.from_department = action_maker.department
		new_doc.from_designation = action_maker.designation
		new_doc.details = details
		new_doc.action_date = frappe.utils.today()
		new_doc.created_by = action_maker.user_id  # Use user_id instead of recipient_email

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
		update_share_permissions(
			outbox_memo, user_id, json.dumps({"read": 1, "write": 0, "share": 0, "submit": 0})
		)
		action_name = new_doc.name
		if reports_to_emp:
			return {
				"message": "Action Success",
				"action_name": action_name,
				"action_maker": reports_to_emp.user_id or "",
			}
		else:
			return {"message": "Action Success", "action_name": action_name, "action_maker": ""}
	else:
		return {"message": "No employee found for the given user ID."}


@frappe.whitelist()
def update_share_permissions(docname, user, permissions):
	share = frappe.get_all(
		"DocShare",
		filters={"share_doctype": "Outbox Memo", "share_name": docname, "user": user},
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


def share_permission_through_route(document, current_employee):
	reports_to = current_employee.reports_to
	if current_employee.user_id != document.recipients[0].recipient_email:
		reports_to_emp = frappe.get_doc("Employee", reports_to)
		# if reports_to_emp != document.recipients[0].recipient_email:
		frappe.share.add(
			doctype="Outbox Memo",
			name=document.name,
			user=reports_to_emp.user_id,
			read=1,
			write=1,
			share=1,
			submit=1,
		)
