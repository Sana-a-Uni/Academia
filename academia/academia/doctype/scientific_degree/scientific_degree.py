# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class ScientificDegree(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        description: DF.Text | None
        scientific_degree_name: DF.Data
    # end: auto-generated types

    def validate(self):
        if not re.match("^[a-zA-Z ']*$", self.scientific_degree_name):
            frappe.throw("Scientific degree should only contain letters and single quotes")


