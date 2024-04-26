# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe import _


class FacultyMemberUniversityandCommunityService(Document):
	def validate(self):
	 if self.date:
            if self.date > frappe.utils.today():
                frappe.throw(_(" Date cannot be in the future"))
