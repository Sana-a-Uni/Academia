# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re
from frappe import _
 
class Journal(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        hindex: DF.Data | None
        impact_factor: DF.Float
        internal_journal: DF.Check
        issn: DF.Data | None
        journal_name: DF.Data
        journal_type: DF.Link | None
        quarter_classification: DF.Literal["", "Q1", "Q2", "Q3", "Q4"]
        website_link: DF.Data | None
    # end: auto-generated types
    def validate(self):
        # Calling functions
        self.validate_url()

        if self.hindex and not re.match("^[0-9]+$", str(self.hindex)):
            frappe.throw(_("H-Index should only contain numbers."))

        if self.issn:
            issn_str = str(self.issn).strip()  # Remove leading/trailing whitespaces
            if not issn_str or not re.match(r"^\d{4}[-\s]?\d{4}$", issn_str):
                # Only allow digits and hyphen
                frappe.throw(_("ISSN should be in the format XXXX-XXXX or XXXX XXXX, where X represents a digit."))

            else:
                # Format the ISSN as XXXX-XXXX
                formatted_issn = re.sub(r"(\d{4})(\d{4})", r"\1-\2", issn_str)
                self.issn = formatted_issn


    # FN: Verifying 'website_link' field
    def validate_url(self):
        # Define a regular expression pattern for validating URLs
        url_pattern = re.compile(r'^(http|https|ftp)://\S+$')
        # Verifying that website_link matches the URL pattern
        if self.website_link:
            if not url_pattern.match(self.website_link):
                frappe.throw(_("Website Link is not valid. Please enter a valid URL starting with http, https, or ftp."))
    # End of the function
