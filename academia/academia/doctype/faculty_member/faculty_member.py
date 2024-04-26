# Copyright (c) 2023, SanU and contributors
# For license information, please see license.txt
from frappe.model.document import Document
import frappe
from frappe import _

class FacultyMember(Document):
    def validate(self):
        if self.date_of_joining_in_university and self.date_of_joining_in_service:
            if self.date_of_joining_in_service >= self.date_of_joining_in_university:
                frappe.throw(_("Date of Service Appointment must be before Date of University Appointment"))
