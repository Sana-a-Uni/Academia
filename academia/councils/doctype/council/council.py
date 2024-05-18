# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Council(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from academia.councils.doctype.council_member.council_member import CouncilMember
        from frappe.types import DF

        administrative_body: DF.Link
        company: DF.Link
        council_name: DF.Data
        get_members_from_other_companies: DF.Check
        members: DF.Table[CouncilMember]
    # end: auto-generated types
 
    def validate(self):
        validate_members(self.members)


def validate_members(members):
    roles, employees = zip(*[(member.member_role, member.employee)
                         for member in members])
    check_employee_duplicate(employees)
    check_council_head_and_reporter_duplication(roles)
    # check if at least one member is a coucil head
    if roles.count(_('Council Head')) < 1:
        frappe.throw(_(f"This Council doesn't have a Council Head"))


# Function to check for member duplicates
def check_employee_duplicate(employees):
    # Iterate through each member
    for employee in employees:
        # Check if the member count is greater than 1, indicating a duplicate
        if employees.count(employee) > 1:
            # Throw an error if duplicates are found
            frappe.throw(_(f"Council members can't be duplicated"))
            
def check_council_head_and_reporter_duplication(roles):
    # Check if the Council Head count is greater than 1, indicating a duplicate
    if roles.count(_('Council Head')) > 1:
        frappe.throw(
            _(f"This Council already has a {_('Council Head')}"))
    elif roles.count(_('Council Reporter')) > 1:
        frappe.throw(
            _(f"This Council already has a {_('Council Reporter')}"))
            
        