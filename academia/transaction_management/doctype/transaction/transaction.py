# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document


class Transaction(Document):
    # pass
    def before_save(self):
        created_by = frappe.get_doc('User', frappe.session.user)
        self.created_by = created_by.name
    


@frappe.whitelist()
def get_transaction_category_requirement(transaction_category):
    requirements = frappe.get_all("Transaction Category  Requirement",
                                   filters={"parent": transaction_category},
                                    )
    return requirements
           
@frappe.whitelist()
def get_transaction_actions(transaction):
    transaction_actions = frappe.get_all('Transaction Action',
                                  filters={'main_transaction': transaction},
                                  fields=['*'],)
    return transaction_actions