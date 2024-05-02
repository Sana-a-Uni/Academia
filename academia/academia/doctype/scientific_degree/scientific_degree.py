# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class ScientificDegree(Document):

    def validate(self):
        if not re.match("^[a-zA-Z ]*$", self.scientific_degree_name):
            frappe.throw("Scientific degree should only contain letters")


