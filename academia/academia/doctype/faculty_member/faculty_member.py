# Copyright (c) 2023, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FacultyMember(Document):
	def autoname(self):
		self.full_name = self.first_name + " " + self.middle_name + " " + self.last_name
