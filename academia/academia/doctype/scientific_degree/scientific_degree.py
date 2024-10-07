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
    pass