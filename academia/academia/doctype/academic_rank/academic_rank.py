# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
import re
class AcademicRank(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        academic_rank_name: DF.Data
        description: DF.Text | None
    # end: auto-generated types
    def validate(self):
        if not re.match("^[A-Za-z\s]+$", self.academic_rank_name):
            frappe.throw("Academic rank name should only contain letters")