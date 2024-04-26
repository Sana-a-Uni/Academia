# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class FacultyMemberScientificQualification(Document):

    def validate(self):
        if not re.match("^[a-zA-Z ]*$", self.general_field):
            frappe.throw("General field should only contain letters")

        if not re.match("^[a-zA-Z ]*$", self.specialist_field):
            frappe.throw("Specialist field should only contain letters")