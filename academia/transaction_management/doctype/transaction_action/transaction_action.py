# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class TransactionAction(Document):
	pass

#   @property
#   def created_by(self):
#        return frappe.get_value("Transaction Action", self.name, "owner")
#   @property
#   def action_date(self):
#        return frappe.get_value("Transaction Action", self.name, "creation")
