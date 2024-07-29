# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re
from frappe import _

class FacultyMemberConferenceandWorkshop(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        description: DF.Text | None
        ends_on: DF.Date | None
        location: DF.Data | None
        name1: DF.Data
        name: DF.Int | None
        parent: DF.Data
        parentfield: DF.Data
        parenttype: DF.Data
        participation_type: DF.Literal["", "Researcher", "Presenter", "Supervisor", "Chairperson", "Participant", "Attendee (Guest)"]
        starts_on: DF.Date | None
    # end: auto-generated types
    pass