# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class TransactionAction(Document):
	pass

@frappe.whitelist()
def redirect_transaction(main_transaction, party, to_department, redirect_to):

	# get document of user by email
	redirected_to = frappe.get_doc("User", redirect_to)

	main_transaction = frappe.get_doc("Transaction", main_transaction)

	create_redirect_action(main_transaction, party, to_department, redirect_to)

	create_user_permission("Transaction", redirect_to, main_transaction)
		
	return f'Transaction redirected successfully to <b> <strong> {redirected_to.username} </strong> </b>'


# @frappe.whitelist()
# def create_user_permission(user, for_value):

# 	user = frappe.get_doc("User", user)
# 	for_value = frappe.get_doc("Transaction", for_value)
	
# 	#TODO: check if the user permission exist 
# 	new_user_permission = frappe.get_doc({
# 		"doctype": "User Permission",
# 		"allow": "Transaction",
# 		"user": user,
# 		"for_value": for_value,
# 		"apply_to_all_doctypes": 1
# 	})
# 	new_user_permission.insert()

# # TODO: create one function for all actions 
# def create_redirect_action(main_transaction, party, to_department, redirect_to):

# 	# create new transaction action for redirect
# 	redirected_transaction = frappe.new_doc("Transaction Action")
# 	redirected_transaction.main_transaction = main_transaction
# 	redirected_transaction.type = "Redirected"
# 	redirected_transaction.party = party
# 	redirected_transaction.to_department = to_department
# 	redirected_transaction.redirected_to = redirect_to
# 	redirected_transaction.sent_date = datetime.now()
# 	redirected_transaction.insert()

# 	return redirect_transaction

# def create_user_permission(allow, user, for_value, permlevel=0):

# 	#TODO: check if the user permission exist 
# 	new_user_permission = frappe.get_doc({
#         "doctype": "User Permission",
#         "allow": allow,
#         "user": user,
#         "for_value": for_value,
#         "apply_to_all_doctypes": 0,
#         "permlevel": permlevel
#     })
# 	new_user_permission.insert()
	
# TODO: add field who receive the transaction
# @frappe.whitelist()
# def receive_transaction(main_transaction):
# 	transaction = frappe.new_doc("Transaction Action")
# 	transaction.main_transaction = main_transaction
# 	transaction.type = "Received"
# 	transaction.receive_date = datetime.now()
# 	transaction.insert()

# 	return "Transaction received successfully"

# TODO: insteade of recieve/sent date make action_date
# but what if we need to calculate the time between receive and action date? maybe its easy

# @frappe.whitelist()
# def approve_transaction(main_transaction):
# 	transaction = frappe.new_doc("Transaction Action")
# 	transaction.main_transaction = main_transaction
# 	transaction.type = "Approved"
# 	transaction.insert()

# 	return "Transaction approved successfully"


# @frappe.whitelist()
# def reject_transaction(main_transaction):
# 	transaction = frappe.new_doc("Transaction Action")
# 	transaction.main_transaction = main_transaction
# 	transaction.type = "Rejected"
# 	transaction.insert()

# 	return "Transaction approved successfully"

# @frappe.whitelist()
# def cancel_transaction_action(doctype, docname):
# 	doc = frappe.get_doc(doctype, docname)
# 	user = doc.redirected_to
# 	doc.status = "Canceled"
# 	doc.save()
# 	doc.cancel()
# 	if user:
# 		user_permission = frappe.get_list(
# 			"User Permission",
# 			filters={
# 				"allow": doctype,
# 				"for_value": doc.redirected_transaction_action,
# 				"user": user
# 			},
# 		)
# 		if user_permission:
# 			frappe.delete_doc("User Permission", user_permission[0].name)
# 			return "Redirect canceled successfully"
# 	else:
# 		return "Document canceled successfully"
