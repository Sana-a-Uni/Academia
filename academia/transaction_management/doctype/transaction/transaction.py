# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document

class Transaction(Document):
    def before_save(self):
        created_by = frappe.get_doc('User', frappe.session.user)
        self.created_by = created_by.name
  
@frappe.whitelist()
def get_transaction_category_requirement(transaction_category):
    requirements = frappe.get_all("Transaction Category  Requirement",
                                   filters={"parent": transaction_category},)
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