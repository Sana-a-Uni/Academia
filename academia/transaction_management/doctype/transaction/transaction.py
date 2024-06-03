# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe # type: ignore
from frappe.model.document import Document # type: ignore
import json

class Transaction(Document):
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