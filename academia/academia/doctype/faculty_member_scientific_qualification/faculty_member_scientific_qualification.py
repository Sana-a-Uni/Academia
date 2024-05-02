# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import re

class FacultyMemberScientificQualification(Document):
    def validate(self):
        if self.starts_on and self.ends_on:
            if self.ends_on <= self.starts_on:
                frappe.throw(_("Date of End must be after Date of Start"))

        if self.ends_on and self.date_of_achievement:
            if self.date_of_achievement <= self.ends_on:
                frappe.throw(_("Date of Achievement must be after End Date"))
        
            if self.date_of_achievement > frappe.utils.today():
                frappe.throw(_("Date of Achievement cannot be in the future"))


        if not re.match("^[a-zA-Z ]*$", self.general_field):
            frappe.throw("General field should only contain letters")

        if not re.match("^[a-zA-Z ]*$", self.specialist_field):
            frappe.throw("Specialist field should only contain letters")

