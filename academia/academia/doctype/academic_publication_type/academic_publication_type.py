# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class AcademicPublicationType(Document):

    def validate(self):
        if not re.match("^[a-zA-Z ]*$", self.publication_type):
            frappe.throw("Publication type should only contain letters")


