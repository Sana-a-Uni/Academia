# Copyright (c) 2025, SanU and contributors
# For license information, please see license.txt
import json

import frappe
from frappe.model.document import Document


class PermissionUpdateTool(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        amended_from: DF.Link | None
        details: DF.Text | None
        new_employee: DF.Link
        old_employee: DF.Link
    # end: auto-generated types

    def on_submit(self):
        # frappe.msgprint("on_submit triggered!")
        update_user_values(
            doctype_name="DocShare",
            field_a="user",
            condition_a_value=self.old_employee,
            new_value_for_field_a=self.new_employee,
            field_b="share_doctype",
            condition_b_values=[
                "Transaction",
                "Transaction New",
                "Inbox Memo",
                "Outbox Memo",
                "Request",
                "Specific Transaction Document"
            ]
        )
        # update_user_values(
        #     doctype_name="Transaction New",
        #     field_a="current_action_maker",
        #     condition_a_value=self.old_employee,
        #     new_value_for_field_a=self.new_employee
        # )
        # update_user_values(
        #     doctype_name="Transaction",
        #     field_a="current_action_maker",
        #     condition_a_value=self.old_employee,
        #     new_value_for_field_a=self.new_employee
        # )
        update_user_values(
            doctype_name="Inbox Memo",
            field_a="current_action_maker",
            condition_a_value=self.old_employee,
            new_value_for_field_a=self.new_employee
        )
        update_user_values(
            doctype_name="Outbox Memo",
            field_a="current_action_maker",
            condition_a_value=self.old_employee,
            new_value_for_field_a=self.new_employee
        )
        update_user_values(
            doctype_name="Specific Transaction Document",
            field_a="current_action_maker",
            condition_a_value=self.old_employee,
            new_value_for_field_a=self.new_employee
        )
        update_user_values(
            doctype_name="Request",
            field_a="current_action_maker",
            condition_a_value=self.old_employee,
            new_value_for_field_a=self.new_employee
        )

	






def update_user_values(
    doctype_name, 
    field_a, 
    condition_a_value, 
    new_value_for_field_a, 
    field_b=None,  # Optional parameter
    condition_b_values=None  # Optional parameter
):
    """
    Updates records in a specified Doctype based on given conditions.

    :param doctype_name: Name of the Doctype to target
    :param field_a: The field to be updated
    :param condition_a_value: The value Field A should match
    :param new_value_for_field_a: The new value to set for Field A
    :param field_b: (Optional) Another field to check conditions against
    :param condition_b_values: (Optional) List of acceptable values for Field B
    """
    # Prepare filters
    filters = {field_a: condition_a_value}  # Always filter by Field A
    if field_b and condition_b_values:  # Add Field B condition if provided
        filters[field_b] = ["in", condition_b_values]
    
    # Fetch records matching the filters
    records = frappe.get_all(
        doctype_name,
        filters=filters,
        fields=["name", field_a]  # Fetch only 'name' and 'field_a' for the records
    )

    # If no records are found, throw a message
    if not records:
        frappe.msgprint(
            f"No records found in {doctype_name} matching the given conditions.",
            title="No Updates Made",
            indicator="green",
        )
        return
    
    # Iterate through records and update Field A
    for record in records:
        frappe.db.set_value(
            doctype_name,
            record["name"],  # Unique identifier of the record
            field_a,
            new_value_for_field_a
        )
        frappe.db.commit()  # Commit each change to the database
    
    # Display a message with the number of updated records
    frappe.msgprint(
        f"Updated {len(records)} records in {doctype_name}.",
        title="Update Successful",
        indicator="green"
    )
