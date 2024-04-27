
from frappe.model.document import Document
import frappe
from frappe import _

from datetime import datetime


class FacultyMember(Document):
    def validate(self):
        today = datetime.now().date()
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




