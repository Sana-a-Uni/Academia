# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe # type: ignore
from frappe.model.document import Document # type: ignore
import json

class Transaction(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from academia.councils.doctype.topic_applicant.topic_applicant import TopicApplicant
        from academia.transaction_management.doctype.transaction_action.transaction_action import TransactionAction
        from academia.transaction_management.doctype.transaction_attachments.transaction_attachments import TransactionAttachments
        from academia.transaction_management.doctype.transaction_recipient.transaction_recipient import TransactionRecipient
        from academia.transaction_management.doctype.transaction_recipients.transaction_recipients import TransactionRecipients
        from frappe.types import DF

        actions: DF.Table[TransactionAction]
        amended_from: DF.Link | None
        applicants_table: DF.Table[TopicApplicant]
        attachments: DF.Table[TransactionAttachments]
        category: DF.Link | None
        company: DF.Link | None
        created_by: DF.Data | None
        description: DF.TextEditor | None
        full_electronic: DF.Check
        include_other_companies: DF.Check
        main_external_entity: DF.Link | None
        priority: DF.Literal["", "Low", "Medium", "High", "Urgent"]
        recipient_designation: DF.Link | None
        recipient_multi_select_table: DF.TableMultiSelect[TransactionRecipient]
        recipients: DF.Table[TransactionRecipients]
        reference_number: DF.Data | None
        start_date: DF.Data | None
        status: DF.Literal["Pending", "Approved", "Rejected"]
        sub_category: DF.Link | None
        sub_external_entity: DF.Link | None
        title: DF.Data | None
        transaction_scope: DF.Literal["In Company", "Among Companies", "With External Entity"]
    # end: auto-generated types
    def on_submit(self):
        for row in self.recipient_multi_select_table:
            user = frappe.get_doc("User", row.recipient)
            create_share(self.name, user.email, 1, 1, 1)
            



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
    parent_category = frappe.db.get_value("Transaction Category", transaction_category, "parent_category")
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

def create_share(docname, user,  read=1, write=0, share=0):
    # Create a share for the document
    share_doc = frappe.share.add(
        doctype="Transaction",
        name=docname,
        user=user,
        read=read,
        write=write,
        share=share
    )

    return share_doc