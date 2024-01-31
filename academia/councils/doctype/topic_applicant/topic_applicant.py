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
        applicant_name: DF.Data | None
        applicant_type: DF.Literal["", "Student", "Academic", "User", "Other"]
        parent: DF.Data
        parentfield: DF.Data
        parenttype: DF.Data
    # end: auto-generated types
    def validate(self):
        applicant_doc = frappe.get_doc(self.applicant_type, self.applicant)
        frappe.throw("Document found555")
        if applicant_doc:
            self.applicant_name = applicant_doc.attribute_name
            frappe.throw("Document found")
        else:
            self.applicant_name = ""
            frappe.throw("Document not found")
