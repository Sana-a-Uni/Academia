# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re
from frappe import _

class ScientificArticle(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from academia.academia.doctype.academic_author.academic_author import AcademicAuthor
        from frappe.types import DF

        article_file: DF.Attach | None
        article_link: DF.Data | None
        date_of_publish: DF.Date | None
        published_in: DF.Link | None
        scientific_article_author: DF.Table[AcademicAuthor]
        title: DF.Data
    # end: auto-generated types
    # Start of validate controller hook
    def validate(self):
        # Calling functions
        self.validate_date()
        self.validate_url()
    # End of validate controller hook

    # FN: validate 'date_of_publish' field
    def validate_date(self):
            today = frappe.utils.today()
            if self.date_of_publish:
                if self.date_of_publish > today:
                    frappe.throw(_("Date of publish cannot be in the future."))
    # End of the function


    # FN: validate 'article_link' field
    def validate_url(self):
        # Define a regular expression pattern for validating URLs
        url_pattern = re.compile(r'^(http|https|ftp)://\S+$')
        # Verifying that article_link matches the URL pattern
        if self.article_link:
            if not url_pattern.match(self.article_link):
                frappe.throw(_("Article Link is not valid. Please enter a valid URL starting with http, https, or ftp."))
    # End of the function

    