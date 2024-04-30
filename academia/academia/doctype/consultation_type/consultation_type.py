# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class ConsultationType(Document):
    def validate(self):
        if not re.match("^[a-zA-Z ]*$", self.consultation_type):
            frappe.throw("Consultation type should only contain letters")
