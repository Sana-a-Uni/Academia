# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class Transaction(Document):   
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from academia.councils.doctype.topic_applicant.topic_applicant import TopicApplicant
        from academia.transaction_management.doctype.transaction_action.transaction_action import TransactionAction
        from academia.transaction_management.doctype.transaction_attachments.transaction_attachments import TransactionAttachments
        from frappe.types import DF

        actions: DF.Table[TransactionAction]
        amended_from: DF.Link | None
        attachments: DF.Table[TransactionAttachments]
        category: DF.Link | None
        client: DF.DynamicLink | None
        client_doctype: DF.Link | None
        company: DF.Link | None
        created_by: DF.Link | None
        description: DF.TextEditor | None
        full_electronic: DF.Check
        priority: DF.Literal["", "Low", "Medium", "High", "Urgent"]
        reference_number: DF.Data | None
        related_to_table: DF.Table[TopicApplicant]
        start_date: DF.Datetime | None
        status: DF.Literal["Pending", "Approved", "Rejected"]
        sub_category: DF.Link | None
        title: DF.Data | None
        transaction_scope: DF.Literal["In Company", "Among Companies", "With External Entity"]
    # end: auto-generated types
    pass     
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

#   @property
#   def created_by(self):
#        return frappe.get_value("Transaction", self.name, "owner")

# @frappe.whitelist()
# def get_transaction_category_requirement(transaction_category):
#     requirements = frappe.get_all("Transaction Category Requirement",
#                                    filters={"parent": transaction_category},)
#     return requirements

@frappe.whitelist()
def get_transaction_category_requirement(transaction_category):
    requirements = []

    # Fetch requirements for the selected transaction category
    transaction_category_requirements = frappe.get_all("Transaction Category  Requirement",
                                                      filters={"parent": transaction_category},
                                                      fields=["name", "file_type", "required"])
    requirements.extend(transaction_category_requirements)

    # Check if the transaction category has a parent category
    parent_category = frappe.db.get_value("Transaction Category", transaction_category, "category_parent")
    if parent_category:
        # Fetch requirements for the parent category
        parent_category_requirements = frappe.get_all("Transaction Category  Requirement",
                                                     filters={"parent": parent_category},
                                                      fields=["name", "file_type", "required"])
        requirements.extend(parent_category_requirements)

    return requirements


@frappe.whitelist()
def update_share_permissions(docname, user, permissions):
    share = frappe.get_all("DocShare", filters={
        "share_doctype": "Transaction",
        "share_name": docname,
        "user": user
    })

    permissions_dict = json.loads(permissions)

    if share:
        # Share entry exists, update the permissions
        share = frappe.get_doc("DocShare", share[0].name)
        share.update(permissions_dict)
        share.save(ignore_permissions=True)
        frappe.db.commit()

    return share
