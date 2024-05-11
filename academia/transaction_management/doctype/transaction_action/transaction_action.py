# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TransactionAction(Document):
	def before_save(self):

		# set a default value for the hidden fields
		if self.outgoing:
			self.from_party = "Department"
			department = frappe.get_doc("Department", "Accounts")
			if department:
				self.from_department = department.name	
		if self.incoming:
			self.to_party = "Department"
			department = frappe.get_doc("Department", "Accounts")
			if department:
				self.to_department = department.name

		for row in self.attachments:
			if not row.attachment_name:
				row.attachment_name = row.attachment_label.replace(" ", "_").lower() + "_file"
		   
@frappe.whitelist()
def get_main_transaction_information(transaction):
    transaction = frappe.get_doc('Transaction', transaction )
    return transaction