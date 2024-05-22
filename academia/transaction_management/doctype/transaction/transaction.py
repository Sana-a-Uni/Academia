# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt


import frappe # type: ignore
from frappe.model.document import Document # type: ignore


class Transaction(Document):
    def before_save(self):

        created_by = frappe.get_doc('User', frappe.session.user)
        self.created_by = created_by.name
    
       
@frappe.whitelist()
def get_transaction_actions(transaction):
    transaction_actions = frappe.get_all('Transaction Action',
                                  filters={'main_transaction': transaction},
                                  fields=['*'],)
    return transaction_actions
  
@frappe.whitelist()
def get_transaction_category_requirement(transaction_category):
    requirements = frappe.get_all("Transaction Category  Requirement",
                                   filters={"parent": transaction_category},)
    return requirements

@frappe.whitelist()
def get_last_transaction_action_status(transaction):
    # Last_transaction_action = frappe.get_last_doc('Transaction Action',
    #                               filters={'main_transaction': transaction})
    # if Last_transaction_action:
    #     return Last_transaction_action.status
    # else:
    #     return ''
    last_transaction_action = frappe.get_list(
        'Transaction Action',
        filters={'main_transaction': transaction},
        fields=['status'],
        order_by='creation DESC',
        limit=1
    )

    if last_transaction_action:
        return last_transaction_action[0].status
    else:
        return ''