# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re

class FacultyMemberTrainingCourse(Document):
    def validate(self):
        if not re.match("^[a-zA-Z ]*$", self.course_name):
            frappe.throw("Course name should only contain letters")
