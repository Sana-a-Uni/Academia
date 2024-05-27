# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

from frappe.model.document import Document
import frappe
from frappe import _
import re
from datetime import datetime


class FacultyMember(Document):
    # Start of validate controller hook
    def validate(self):
        today = datetime.now().date()
        # Calling functions
        self.validate_duplicate_employee()
        self.validate_date()
        self.validate_url()
    # End of validate controller hook
   
    # FN: validate duplicate 'employee' field
    def validate_duplicate_employee(self):
          if self.employee:
            exist_employee = frappe.get_value("Faculty Member", {"employee": self.employee, "name": ["!=", self.name]}, "faculty_member_name")
            if exist_employee:
                frappe.throw(f"Employee {self.employee} is already assigned to {exist_employee}")    
    # End of the function

    # FN: validate 'date_of_joining_in_university' and 'date_of_joining_in_service' fields
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
    # End of the function

    # FN: validate 'google_scholar_profile_link' field
    def validate_url(self):
        url_pattern = re.compile(r'^(http|https|ftp)://\S+$')
        if self.google_scholar_profile_link:
            if not url_pattern.match(self.google_scholar_profile_link):
                frappe.throw("Google Scholar Profile Link is not valid. Please enter a valid URL starting with http, https, or ftp")
    # End of the function

		



