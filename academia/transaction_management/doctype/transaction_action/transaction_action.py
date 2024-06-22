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
		type: DF.Literal["", "Redirected", "Approved", "Rejected", "Canceled", "Council"]
	# end: auto-generated types
	def on_submit(self):
		# TODO: change the fields to virtual
		# self.action_date = frappe.utils.format_datetime(
		# 					self.creation, 
		# 					format_string='dd MMM yyyy, HH:mm:ss'
		# 				)
		# self.created_by = self.owner

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