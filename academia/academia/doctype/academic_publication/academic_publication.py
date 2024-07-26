# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

from frappe.model.document import Document
import frappe
from frappe import _
import re


class AcademicPublication(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from academia.academia.doctype.academic_author.academic_author import AcademicAuthor
        from frappe.types import DF

        academic_publication_author: DF.Table[AcademicAuthor]
        apa_citation: DF.SmallText
        date_of_publish: DF.Date | None
        from_page: DF.Data | None
        page_numbers: DF.Data | None
        publication_file: DF.Attach | None
        publication_link: DF.Data | None
        publication_type: DF.Link | None
        published_in: DF.Link | None
        title: DF.Data
        to_page: DF.Data | None
    # end: auto-generated types
    # Start of validate controller hook
    def validate(self):
        # Calling functions
        self.validate_page_numbers()
        self.validate_url()
        self.validate_date()
    # End of validate controller hook

    # FN: validating 'from_page', 'to_page' and 'page_numbers' fields
    def validate_page_numbers(self):
        # validating that both fields are filled, not just one
        if (not self.from_page and self.to_page) or (self.from_page and not self.to_page):
            frappe.throw("Please fill both 'From Page' and 'To Page' fields.")
        # validating that both fields have non-null values
        elif self.from_page and self.to_page:
            # validating that both fields contain only numbers and this - character
            if not self.from_page.replace('-', '').isdigit() or not self.to_page.replace('-', '').isdigit():
                frappe.throw("Page numbers must be integer.")
            # validating that both fields do not contain negative values 
            elif int(self.from_page) < 0 or int(self.to_page) < 0:
                frappe.throw("Page numbers must be positive.")
            # validating that the first page is not greater than the last page
            elif int(self.from_page) > int(self.to_page):
                frappe.throw("First page must be less than last page.")
            # writing the correct values in a specific format
            else:
                if int(self.from_page) == int(self.to_page):
                    self.page_numbers = self.from_page
                else:
                    self.page_numbers = f"{self.from_page} - {self.to_page}"
        # validating that both fields have null values
        else:
            self.page_numbers = '0'
            self.from_page = '0'
            self.to_page = '0'
    # End of the function


    # FN: validate 'publication_link' field
    def validate_url(self):
        url_pattern = re.compile(r'^(http|https|ftp)://\S+$')
        if self.publication_link:
            if not url_pattern.match(self.publication_link):
                frappe.throw("Publication Link is not valid. Please enter a valid URL starting with http, https, or ftp")
    # End of the function

    # FN: validate 'date_of_publish' field
    def validate_date(self):
            if self.date_of_publish:
                if self.date_of_publish > frappe.utils.today():
                    frappe.throw(_("Date of publish must be less than or equal to today's date"))
    # End of the function



