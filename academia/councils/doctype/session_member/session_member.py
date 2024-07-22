# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SessionMember(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        alternative_employee: DF.Link | None
        attendance: DF.Literal["Attend", "Absent with Excuse", "Absent without Excuse"]
        employee: DF.Link
        excuse: DF.Data | None
        member_name: DF.Data | None
        member_role: DF.Literal["", "Council Head", "Council Member", "Council Reporter"]
        parent: DF.Data
        parentfield: DF.Data
        parenttype: DF.Data
    # end: auto-generated types
    pass

    @property
    def member_name(self):
        return frappe.get_value('Employee', self.employee, 'employee_name')
