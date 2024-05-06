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
        members: DF.Table[CouncilMember]
    # end: auto-generated types
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from academia.councils.doctype.council_member.council_member import CouncilMember
        from frappe.types import DF

        administrative_body: DF.Data | None
        council_members: DF.Table[CouncilMember]
        council_name: DF.Data
	# end: auto-generated types
 
 
    def validate(self):
        roles, members = zip(*[(member.member_role, member.member_name) for member in self.members])
        # Check for member duplicates
        if self.check_member_duplicate(members):
            # Throw an error if duplicates are found
            frappe.throw(_(f"Council members can't be duplicated"))

        # check if head and reporater roles are duplicated
        resultOfRoleDuplication = self.check_council_head_and_reporter_duplication(roles)
        if resultOfRoleDuplication == _('Council Head') or resultOfRoleDuplication == _('Council Reporter'):
            frappe.throw(_(f"This Council already has a {resultOfRoleDuplication}"))
            
        # check if at least one member is a coucil head
        if roles.count(_('Council Head')) < 1:
            frappe.throw(_(f"This Council doesn't have a Council Head"))

    # Function to check for member duplicates
    def check_member_duplicate(self, members):
        # Iterate through each member
        for member in members:
            # Check if the member count is greater than 1, indicating a duplicate
            if members.count(member) > 1:
                return True
            
    def check_council_head_and_reporter_duplication(self, roles):
        # Iterate through each member
        for role in roles:
            # Check if the member count is greater than 1, indicating a duplicate
            if roles.count(_('Council Head')) > 1:
                return _('Council Head')
            elif roles.count(_('Council Reporter')) > 1:
                return _('Council Reporter')
        