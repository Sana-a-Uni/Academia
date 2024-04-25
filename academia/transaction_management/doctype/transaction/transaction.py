# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document


class Transaction(Document):
    def before_save(self):
        if self.outgoing:
            self.from_party = "Department"
            department = frappe.get_doc("Department", "Accounts")
            if department:
                self.from_department = department.name	
        if self.incoming:
            self.to_party = "Department"
            department = frappe.get_doc("Department", "Accounts")
            if department:
                self.to_department = department.name	


