# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Session(Document):
		@frappe.whitelist()
		def get_linked_council(self,docname):
			# Check if the 'Council' document with the given docname exists in the database
			if frappe.db.exists('Council', docname):
				# Retrieve and return the 'Council' document as a Frappe document object
				return frappe.get_doc('Council', docname)
