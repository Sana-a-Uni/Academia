# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class Authority(Document):

    def validate(self):
        if not re.match("^[a-zA-Z ]*$", self.authority_name):
            frappe.throw("Authority name should only contain letters")

