# Copyright (c) 2023, SanU and contributors
# For license information, please see license.txt

from frappe.model.document import Document
import frappe
import re

class FacultyMember(Document):
    # def validate(self):
    #     self.set_image_read_only()

    # def set_image_read_only(self):
    #     frappe.db.sql("UPDATE `tabDocField` SET `read_only` = 1 WHERE `parent` = %s AND `field_name` = 'image'", self.doctype)
    pass