# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
from frappe import _


class FacultyMemberAcademicExperience(Document):
    def validate(self):
        if self.hiring_date:
            if self.hiring_date > frappe.utils.today():
                frappe.throw(_("Hiring date cannot be in the future"))


