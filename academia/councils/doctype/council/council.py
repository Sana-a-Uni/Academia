# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.permissions import add_user_permission


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
    
    def before_save(self):
        self.update_permissions()

    def update_permissions(self):
        """
		Update the user permissions for the Council Head and Council Reporter.

		This method performs the following actions:
		1. Retrieves a list of Council members with their employee, member role, and user ID.
		2. Adds user permissions for the "Council" entity and the current Council's name for head and reporter.
		3. Adds the appropriate roles ("Council Head" or "Council Reporter") to the user if the role is not already assigned.
		4. Removes the user permissions and roles for any users who are no longer Head or Reporter.

		The method ensures that the user permissions and roles are kept up-to-date with the current Council group membership.
		"""
		# Get a list of Council members with their employee, member role, and user ID
        members = [{"employee": member.employee, "member_role": member.member_role, "user_id": frappe.get_value(
            "Employee", member.employee, "user_id")} for member in self.members if member.member_role == _("Council Head") or member.member_role == _("Council Reporter")]
        
        # Add user permissions and roles for head and reporter
        for member in members:
            # Check if the user permission already exists
            employee_user_permission_exists = frappe.db.exists(
                "User Permission", {
                    "allow": "Council", "for_value": self.name, "user": member['user_id']}
            )
            if not employee_user_permission_exists:
                add_user_permission("Council", self.name, member['user_id'])
                user = frappe.get_doc("User", member['user_id'])
                user.flags.ignore_permissions = True
                
				# Add the appropriate role if the user doesn't have it
                if member['member_role'] not in user.get("roles"):
                    user.add_roles(member['member_role'])
                    
		# Get user_id members
        users = [member['user_id'] for member in members]
        
		# Remove user permissions and roles for users who are no longer Head or Reporter
        old_user_permissions = frappe.get_all("User Permission", filters={
                                              "allow": "Council", "for_value": self.name, "user": ["not in", users]}, fields=["name", "user"])
        for old_user_permission in old_user_permissions:
            user = frappe.get_doc("User", old_user_permission.user)
            user.remove_roles("Council Head", "Council Reporter")
            frappe.delete_doc("User Permission", old_user_permission.name)


def validate_members(members):
    roles, employees = zip(
        *[(member.member_role, member.employee) for member in members])
    check_employee_duplicate(employees)
    check_council_head_and_reporter_duplication(roles)
    # check if at least one member is a coucil head
    if roles.count(_("Council Head")) < 1:
        frappe.throw(_("This Council doesn't have a Council Head"))


# Function to check for member duplicates
def check_employee_duplicate(employees):
    # Iterate through each member
    for employee in employees:
        # Check if the member count is greater than 1, indicating a duplicate
        if employees.count(employee) > 1:
            # Throw an error if duplicates are found
            frappe.throw(_("Council members can't be duplicated"))


def check_council_head_and_reporter_duplication(roles):
    # Check if the Council Head count is greater than 1, indicating a duplicate
    if roles.count(_("Council Head")) > 1:
        frappe.throw(_("This Council already has a Council Head"))
    elif roles.count(_("Council Reporter")) > 1:
        frappe.throw(_("This Council already has a Council Reporter"))
