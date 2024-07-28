import frappe
from frappe.model.document import Document
import re
from frappe import _

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
        # Debugging: Print the value of the scientific degree field
        # frappe.msgprint(f"Validating scientific degree: {self.scientific_degree_name}")

        # Updated pattern to include both types of single quotes
        pattern = r"^[a-zA-Z\s\-\(\)\'’\u00C0-\u00FF\u0600-\u06FF]+$"

        if not re.match(pattern, self.scientific_degree_name):
            frappe.throw(_("Scientific degree should only contain letters, spaces, hyphens, parentheses, and single quotes."))
