# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class Nationality(Document):
    def validate(self):
        if not re.match("^[a-zA-Z ]*$", self.nationality_name):
            frappe.throw("Nationality name should only contain letters")