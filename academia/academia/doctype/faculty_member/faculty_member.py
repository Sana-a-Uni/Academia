# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

from frappe.model.document import Document
import frappe
from frappe import _
import re


from datetime import datetime


class FacultyMember(Document):

    def validate(self):
        today = datetime.now().date()
        # Calling functions
        self.validate_date()
        self.validate_url()

    def validate_date(self):

        if self.date_of_joining_in_university and self.date_of_joining_in_service:
            # "Converting the date of appointment in service to a date "
            date_of_joining_in_service = datetime.strptime(self.date_of_joining_in_service, "%Y-%m-%d").date()
            date_of_joining_in_university = datetime.strptime(self.date_of_joining_in_university, "%Y-%m-%d").date()
            #  "Ensure that the date of appointment in service is before the date of appointment in the university."
            if date_of_joining_in_service >= date_of_joining_in_university:
                frappe.throw(_("Date of Service Appointment must be before Date of University Appointment"))

            elif date_of_joining_in_service > today:
                frappe.throw(_("Date of Service Appointment cannot be after today's date"))
            elif date_of_joining_in_university > today:
                frappe.throw(_("Date of University Appointment cannot be after today's date"))


    # FN: Verifying 'google_scholar_profile_link' field
    def validate_url(self):
        # Define a regular expression pattern for validating URLs
        url_pattern = re.compile(r'^(http|https|ftp)://\S+$')
        # Verifying that google_scholar_profile_link matches the URL pattern
        if self.google_scholar_profile_link:
            if not url_pattern.match(self.google_scholar_profile_link):
                frappe.throw("Google Scholar Profile Link is not valid. Please enter a valid URL starting with http, https, or ftp")
    # End of the function

