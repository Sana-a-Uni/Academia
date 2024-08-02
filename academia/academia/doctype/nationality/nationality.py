# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re
from frappe import _

class Nationality(Document):
    def validate(self):
        pattern = "^[a-zA-Z\u0600-\u06FF ]*$"
        if not re.match(pattern, self.nationality_name):
            frappe.throw(_("Nationality name should only contain letters."))