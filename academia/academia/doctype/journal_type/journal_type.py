# # Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re
from frappe import _

class JournalType(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        journal_type: DF.Data
        journal_weight: DF.Int
    # end: auto-generated types

    def validate(self):
        self.validate_journal_weight()

    def validate_journal_weight(self):   
        if self.journal_weight and not re.match("^[0-9]+$", str(self.journal_weight)):
            frappe.throw(_("Journal Weight should only contain numbers."))
    
