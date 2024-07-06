# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class TransactionAction(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.transaction_management.doctype.transaction_recipients.transaction_recipients import TransactionRecipients
		from frappe.types import DF

		action_date: DF.Data | None
		amended_from: DF.Link | None
		created_by: DF.Data | None
		details: DF.Text | None
		from_company: DF.Data | None
		from_department: DF.Data | None
		from_designation: DF.Data | None
		recipients: DF.Table[TransactionRecipients]
		transaction: DF.Link | None
		type: DF.Literal["Redirected", "Approved", "Rejected", "Canceled", "Council"]
	# end: auto-generated types
	def on_submit(self):
		self.action_date = frappe.utils.format_datetime(
							self.creation, 
							format_string='dd MMM yyyy, HH:mm:ss'
						)
		self.created_by = self.owner

        # make a read, write, share permissions for reciepents
		for row in self.recipients:
			user = frappe.get_doc("User", row.recipient_email)
			frappe.share.add(
				doctype = "Transaction",
				name = self.transaction,
				user = user.email,
				read = 1,
				write = 1,
				share = 1
			)


import frappe

@frappe.whitelist()
def get_recipients(transaction_name):
    actions = frappe.get_all("Transaction Action",
                             filters={
                                "transaction": transaction_name,
                                "docstatus": 1
                             },
                             fields=["name"])

    recipients_parent = [a.name for a in actions]
    recipients_parent.append(transaction_name)  # Add transaction_name to recipients_parent list


    recipients = frappe.get_all("Transaction Recipients",
                                filters={"parent": ["in", recipients_parent]},
                                fields=["recipient_email"],
                                order_by="creation")

    recipient_emails = [r.recipient_email for r in recipients]

    return recipient_emails

@frappe.whitelist()
def get_transaction_actions(transaction_name):
    # """
    # Retrieves all the Transaction Action documents associated with the given Transaction document.
    
    # Args:
    #     transaction_name (str): Name of the Transaction document.
        
    # Returns:
    #     List[dict]: List of dictionaries representing the Transaction Action documents.
    # """

	# transaction_action = frappe.qb.DocType('Transaction Action')
	# transaction_recipients = frappe.qb.DocType('Transaction Recipients')


	# transaction_actions = frappe.get_all(
    #     "Transaction Action",
    #     filters={
    #         "transaction": transaction_name
    #     },
    #     fields=[
	# 		"name", 
	# 		"type", 
	# 		"details", 
	# 		"creation"
	# 		# to get recipients with all document
	# 		"(SELECT * FROM `tabTransaction Recipients` WHERE parenttype='Transaction Action' AND parent = `tabTransaction Action`.name) as recipients"
	# 		],
	# 	order_by="creation DESC",
    # )
	# transaction_actions = frappe.db.sql(
	# 	f"""
	# 	SELECT `name`,
	# 	FROM `tabTransaction Action`
	# 	WHERE `transaction` == {transaction_name}
	# 	"""
	# )
	# return transaction_actions

	# HasRole = frappe.qb.DocType('Has Role')
	# CustomRole = frappe.qb.DocType('Custom Role')

	# query = (frappe.qb.from_(HasRole)
	# 	.inner_join(CustomRole)
	# 	.on(CustomRole.name == HasRole.parent)
	# 	.select(CustomRole.page, HasRole.parent, HasRole.role))

	query = """
    SELECT ta.name AS action_name,ta.type AS type, GROUP_CONCAT(tr.recipient_email SEPARATOR ', ') AS recipients
    FROM `tabTransaction Action` AS ta
    LEFT JOIN `tabTransaction Recipients` AS tr ON ta.name = tr.parent
    WHERE ta.transaction = %(transaction_name)s
    GROUP BY ta.name
	ORDER BY ta.creation DESC
	"""

	result = frappe.db.sql(query, {"transaction_name": transaction_name}, as_dict=True)
	return result


# def share_permission_through_route(document, current_employee):
#     employee = frappe.get_doc("Employee", current_employee)
#     reports_to = employee.reports_to
#     reports_to_emp = frappe.get_doc("Employee", reports_to)
#     frappe.share.add(
#                 doctype = "Transaction",
#                 name = document.name,
#                 user = reports_to_emp.user_id,
#                 read = 1,
#                 write = 1,
#                 share = 1
#             )

@frappe.whitelist()
def get_next_through_route():
	user = frappe.session.user
	user_doc = frappe.get_doc("User", user)
	current_employee = user_doc.employee

		
	employee = frappe.get_doc("Employee", current_employee)
	reports_to = employee.reports_to
	reports_to_emp = frappe.get_doc("Employee", reports_to)
	# return reports_to_emp
	frappe.msgprint(reports_to)


