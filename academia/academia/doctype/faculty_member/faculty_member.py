# Copyright (c) 2023, SanU and contributors
# For license information, please see license.txt

from frappe.model.document import Document
import frappe
import re

class FacultyMember(Document):
    def autoname(self):
        self.full_name = self.first_name + " " + self.middle_name + " " + self.last_name

    def validate(self):

        if not re.match("^[a-zA-Z ]*$", self.first_name):
            frappe.throw("First name should only contain letters")

        if not re.match("^[a-zA-Z ]*$", self.middle_name):
            frappe.throw("Middle name should only contain letters")

        if not re.match("^[a-zA-Z ]*$", self.last_name):
            frappe.throw("Last name should only contain letters")


