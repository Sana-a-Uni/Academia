# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import re
class FacultyMemberActivity(Document):
    def validate(self):
        if self.date:
            if self.date > frappe.utils.today():
                frappe.throw(_("Date cannot be in the future"))


        if not re.match("^[a-zA-Z ]*$", self.activity_name):
            frappe.throw("Activity name should only contain letters")

        if not re.match("^[a-zA-Z ]*$", self.organization_name):
            frappe.throw("Organization name should only contain letters")

