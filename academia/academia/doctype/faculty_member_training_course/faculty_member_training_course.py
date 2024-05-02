# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re
from frappe import _


class FacultyMemberTrainingCourse(Document):
    def validate(self):
        if self.starts_on and self.ends_on:
            if self.ends_on <= self.starts_on:
                frappe.throw(_("Date of End must be after Date of Start"))

        if not re.match("^[a-zA-Z ]*$", self.course_name):
            frappe.throw("Course name should only contain letters")

