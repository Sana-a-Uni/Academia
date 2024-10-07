# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re
from frappe import _


class FacultyMemberTrainingCourse(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        as_a_trainer: DF.Check
        certification: DF.Attach | None
        course_name: DF.Data
        description: DF.Text | None
        ends_on: DF.Date | None
        location: DF.Data | None
        name: DF.Int | None
        parent: DF.Data
        parentfield: DF.Data
        parenttype: DF.Data
        starts_on: DF.Date | None
    # end: auto-generated types
    pass