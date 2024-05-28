# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Transaction(Document):
    def before_save(self):
        created_by = frappe.get_doc('User', frappe.session.user)
        self.created_by = created_by.name
    
       
# @frappe.whitelist()
# def get_transaction_actions(transaction):
#     transaction_actions =  frappe.get_all(
#             'Transaction Action',
#             filters={'main_transaction': transaction},
#             fields=['*'],
#             order_by='creation'
#         )
#     return transaction_actions
  
@frappe.whitelist()
def get_transaction_category_requirement(transaction_category):
    requirements = frappe.get_all("Transaction Category  Requirement",
                                   filters={"parent": transaction_category},)
    return requirements

# @frappe.whitelist()
# def get_last_transaction_action_type(transaction):
#     # Last_transaction_action = frappe.get_last_doc('Transaction Action',
#     #                               filters={'main_transaction': transaction})
#     # if Last_transaction_action:
#     #     return Last_transaction_action.status
#     # else:
#     #     return ''
#     last_transaction_action = frappe.get_list(
#         'Transaction Action',
#         filters={'main_transaction': transaction},
#         fields=['type'],
#         order_by='creation desc',
#         limit=1
#     )

#     if last_transaction_action:
#         return last_transaction_action[0].type
#     else:
#         return ''
    
# @frappe.whitelist()
# def render_vertical_path(transaction):
#         # Assuming your template file is named "vertical_path.html"
#         # Get the directory path of the Pytho   n file
       
#         # template_path="/home/xair/frappe-bench/apps/academia/academia/templates/vertical_path.html"
#         # # Load the template file
#         # with open(template_path, "r") as file:
#         #     template_content = file.read()

#         # # Create a Jinja template object
#         # template = Template(template_content)

#         # # Fetch data from the "Transaction Action" doctype??
#         # transaction_actions = frappe.get_all("Transaction Action", filters={}, fields=["redirected_to"])
        

#         # # Define the context variables with the fetched data
#         # context = {
#         #     "steps": transaction_actions
#         # }
        
#         # # Render the template
#         # rendered_html = template.render(context)
#         document = frappe.get_doc("Transaction", transaction)
#         #frappe.msgprint(document)
#         # Assign the rendered HTML to the HTML field in the document
#         #document.summary.options = rendered_html
    
#     # Update the options of the HTML field
#         document.set("summary", "hello")
#         document.set("summary_section", 0)
#         # document.summary_section.hidden = 0

#     # Save the changes
#         document.save()
#         return document


def get_permission_query(doctype, meta, role_permissions, for_list_view=False):
    if frappe.session.user != "Administrator":
        # Get the transaction IDs that the current user has access to
        transaction_ids = frappe.db.get_all(
            "Transaction Action",
            filters={
                "redirected_to": frappe.session.user
            },
            pluck="main_transaction"
        )

        # Construct the query based on whether it's for the list view or not
        if for_list_view:
            return """(`tabTransaction`.`created_by` = '{0}' OR `tabTransaction`.`name` IN ({1}))""".format(
                frappe.session.user,
                ", ".join([f"'{tid}'" for tid in transaction_ids])
            )
        else:
            return """(`tabTransaction`.`name` IN ({0}))""".format(
                ", ".join([f"'{tid}'" for tid in transaction_ids])
            )
    else:
        return None