# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re


class ScientificArticle(Document):
    # Start of validate controller hook
    def validate(self):
        # Calling functions
        self.validate_string()
        self.validate_date()
        self.validate_url()
    # End of validate controller hook

    # FN: validate 'title' field
    def validate_string(self):
        if not re.match("^[a-zA-Z ]*$", str(self.title)):
            frappe.throw("Article Title should only contain letters and spaces")
    # End of the function

    # FN: validate 'date_of_publish' field
    def validate_date(self):
        if self.date_of_publish:
            if self.date_of_publish > frappe.utils.today():
                frappe.throw("Date of publish cannot be in the future")
    # End of the function


    # FN: validate 'article_link' field
    def validate_url(self):
        # Define a regular expression pattern for validating URLs
        url_pattern = re.compile(r'^(http|https|ftp)://\S+$')
        # Verifying that article_link matches the URL pattern
        if self.article_link:
            if not url_pattern.match(self.article_link):
                frappe.throw("Article Link is not valid. Please enter a valid URL starting with http, https, or ftp")
    # End of the function

    