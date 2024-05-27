# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TopicApplicant(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        applicant: DF.DynamicLink
        applicant_type: DF.Literal["", "Student", "Academic", "User", "Other"]
        parent: DF.Data
        parentfield: DF.Data
        parenttype: DF.Data
    # end: auto-generated types
    @property
    def applicant_name(self):
        
        # Fetch both 'first_name' and 'last_name' in one database call
        fields = frappe.get_value(self.applicant_type, self.applicant, ["first_name", "last_name"],as_dict=1)

        if fields:
            # Combine first and last name to form full name
            return f"{fields.get('first_name', '')} {fields.get('last_name', '')}".strip()
        else:
            # Handle cases where no data is found
            return "Name Not Set"
