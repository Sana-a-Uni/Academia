# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re


class Journal(Document):
    def validate(self):
        # Calling functions
        self.validate_url()


    # FN: Verifying 'website_link' field
    def validate_url(self):
        # Define a regular expression pattern for validating URLs
        url_pattern = re.compile(r'^(http|https|ftp)://\S+$')
        # Verifying that website_link matches the URL pattern
        if self.website_link:
            if not url_pattern.match(self.website_link):
                frappe.throw("Website Link is not valid. Please enter a valid URL starting with http, https, or ftp")
    # End of the function
