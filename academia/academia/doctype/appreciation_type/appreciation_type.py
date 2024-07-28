# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re
from frappe import _

class AppreciationType(Document):
    def validate(self):
        if not re.match("^[a-zA-Z ]*$", self.appreciation_type):
            frappe.throw(_("Appreciation type should only contain letters."))