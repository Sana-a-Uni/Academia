# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

from frappe.model.document import Document
import frappe
import re

class ScientificArticle(Document):
    def validate(self):
        
        if not re.match("^[a-zA-Z ]*$", str(self.supervisor_name)):
            frappe.throw("Supervisor name should only contain letters and spaces")
        
        if not re.match("^[a-zA-Z ]*$", str(self.publisher_name)):
            frappe.throw("Publisher name should only contain letters and spaces")

