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

        administrative_body: DF.Data | None
        council_members: DF.Table[CouncilMember]
        council_name: DF.Data
	# end: auto-generated types
 
 
    def validate(self):
        # Check for member duplicates
        if self.check_member_duplicate():
            # Throw an error if duplicates are found
            frappe.throw(_(f"Council members can't be duplicated"))
    # Function to check for member duplicates
    def check_member_duplicate(self):
        # Extract member names from the members field
        members = [member.member_name for member in self.members]
        
        # Iterate through each member
        for member in members:
            # Check if the member count is greater than 1, indicating a duplicate
            if members.count(member) > 1:
                return True
    