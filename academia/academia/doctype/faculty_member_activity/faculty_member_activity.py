# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class FacultyMemberActivity(Document):
    
    def validate(self):
        if not re.match("^[a-zA-Z ]*$", self.activity_name):
            frappe.throw("Activity name should only contain letters")

        if not re.match("^[a-zA-Z ]*$", self.organization_name):
            frappe.throw("Organization name should only contain letters")
            

