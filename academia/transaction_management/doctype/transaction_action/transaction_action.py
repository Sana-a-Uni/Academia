# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class TransactionAction(Document):
	def before_save(self):
		for row in self.attachments:
			if not row.attachment_name:
				row.attachment_name = row.attachment_label.replace(" ", "_").lower() + "_file"
		   
@frappe.whitelist()
def get_main_transaction_information(transaction):
    transaction = frappe.get_doc('Transaction', transaction )
    return transaction

@frappe.whitelist()
def redirect_transaction(doctype, docname, party, to_department, redirect_to, permlevel=0):

	current_transaction = frappe.get_doc(doctype, docname)

	# create new transaction action to redirect it
	redirected_transaction = frappe.new_doc("Transaction Action")
	redirected_transaction.main_transaction = current_transaction.main_transaction
	redirected_transaction.priority = current_transaction.priority
	redirected_transaction.status = "Open"
	redirected_transaction.full_electronic = current_transaction.full_electronic

	attachments = []
    
	# Iterate over the attachments in the current transaction
	for attachment in current_transaction.attachments:
		attachment_dict = frappe.new_doc("Transaction Attachments")
		attachment_dict.attachment_name = attachment.attachment_name
		attachment_dict.attachment_label = attachment.attachment_label
		attachment_dict.file = attachment.file
		attachments.append(attachment_dict)

	# Assign the attachments to the redirected transaction
	redirected_transaction.set("attachments", attachments)

	redirected_transaction.insert()
	
	redirected_transaction_user_permission = frappe.get_doc({
        "doctype": "User Permission",
        "user": redirect_to,
        "allow": doctype,
        "for_value": redirected_transaction,
        "apply_to_all_doctypes": 0,
        "permlevel": permlevel
    })
	redirected_transaction_user_permission.insert()

	main_transaction = frappe.get_doc("Transaction", current_transaction.main_transaction)
	# Check if the user permission already exists
	existing_permission = frappe.get_all(
		"User Permission",
		filters={
			"user": redirect_to,
			"allow": "Transaction",
			"for_value": main_transaction
		},
		fields=["name"],
		limit=1
	)

	if not existing_permission:
		main_transaction_user_permission = frappe.get_doc({
			"doctype": "User Permission",
			"user": redirect_to,
			"allow": "Transaction",
			"for_value": main_transaction,
			"apply_to_all_doctypes": 0,
			"permlevel": permlevel
		})

		main_transaction_user_permission.insert()
		
	party = frappe.get_doc("DocType", party)

	to_department = frappe.get_doc(party.name, to_department)
	

	# change the transaction action to be submitted
	current_transaction.status = "Redirected"
	current_transaction.redirected_transaction_action = redirect_transaction
	current_transaction.party = party
	current_transaction.to_department = to_department
	current_transaction.redirected_to = redirect_to
	current_transaction.sent_date = datetime.now()
	current_transaction.save()

	current_transaction.submit()

	# get document of user by email
	redirected_to = frappe.get_doc("User", redirect_to)
	return f'Transaction redirected successfully to <b> <strong> {redirected_to.username} </strong> </b>'

@frappe.whitelist()
def approve_transaction(doctype, docname):
	# change the transaction action to be submitted
	doc = frappe.get_doc(doctype, docname)
	doc.status = "Approved"
	doc.save()
	doc.submit()

	return "Transaction approved successfully"


@frappe.whitelist()
def reject_transaction(doctype, docname):
	# change the transaction action to be submitted
	doc = frappe.get_doc(doctype, docname)
	doc.status = "Rejected"
	doc.save()
	doc.submit()

	return "Transaction approved successfully"

@frappe.whitelist()
def cancel_transaction_action(doctype, docname):
	doc = frappe.get_doc(doctype, docname)
	user = doc.redirected_to
	doc.cancel()

	if user:
		user_permission = frappe.get_list(
			"User Permission",
			filters={
				"allow": doctype,
				"for_value": doc.redirected_transaction_action,
				"user": user
			},
		)
		if user_permission:
			frappe.delete_doc("User Permission", user_permission[0].name)
			return "Redirect canceled successfully"
	else:
		return "Document canceled successfully"
