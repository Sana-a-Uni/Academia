# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
import re
class AcademicRank(Document):
    def validate(self):
        if not re.match("^[A-Za-z\s]+$", self.academic_rank_name):
            frappe.throw("Academic rank name should only contain letters")