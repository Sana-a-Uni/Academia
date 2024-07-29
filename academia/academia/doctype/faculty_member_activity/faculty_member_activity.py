# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import re

class FacultyMemberActivity(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        activity_name: DF.Data
        date: DF.Date | None
        description: DF.Text | None
        location: DF.Data | None
        name: DF.Int | None
        organization_name: DF.Data | None
        parent: DF.Data
        parentfield: DF.Data
        parenttype: DF.Data
    # end: auto-generated types
    pass