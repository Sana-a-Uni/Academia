# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class AcademicPublicationType(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        description: DF.Text | None
        publication_type: DF.Data
    # end: auto-generated types

    def validate(self):
        if not re.match("^[a-zA-Z ]*$", self.publication_type):
            frappe.throw("Publication type should only contain letters")


