# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt


import frappe # type: ignore
from frappe.model.document import Document # type: ignore


class Transaction(Document):
    def before_save(self):
        # Get the list of roles for the current user
        user_roles = frappe.get_roles(frappe.session.user)
        
        # Check if 'Employee' role is in the list of user roles
        if 'Employee' in user_roles:
            # Fetch the employee record linked to the user
            employee_record = frappe.get_all('Employee', filters={'user_id': frappe.session.user}, fields=['department'])
            
            # If an employee record is found and a department is assigned
            if employee_record and employee_record[0].get('department'):
                department = employee_record[0].get('department')
            else:
                # Default to 'Accounts' department if no department is assigned
                department = 'Accounts'
        else:
            # Default to 'Accounts' department if user is not an employee
            department = 'Accounts'

        # Assign the department to the transaction
        if self.outgoing:
            self.from_party = "Department"
            self.from_department = department

        if self.incoming:
            self.to_party = "Department"
            self.to_department = department

        # Process attachments
        for row in self.attachments:
            if not row.attachment_name:
                row.attachment_name = row.attachment_label.replace(" ", "_").lower() + "_file"


# class Transaction(Document):
#     def before_save(self):
#         if self.outgoing:
#             self.from_party = "Department"
#             department = frappe.get_doc("Department", "Accounts")
#             if department:
#                 self.from_department = department.name	
#         if self.incoming:
#             self.to_party = "Department"
#             department = frappe.get_doc("Department", "Accounts")
#             if department:
#                 self.to_department = department.name
    
#         for row in self.attachments:
#             if not row.attachment_name:
#                 row.attachment_name = row.attachment_label.replace(" ", "_").lower() + "_file"
		   
           
@frappe.whitelist()
def get_associated_transactions(associated_transaction):
    linked_transactions = []
    get_linked_transactions(associated_transaction, linked_transactions)
    linked_transactions.reverse()  # Reverse the list to get the oldest transactions first
    return linked_transactions

def get_linked_transactions(associated_transaction, linked_transactions):
    transactions = frappe.get_all('Transaction',
                                  filters={'name': associated_transaction},
                                  fields=['*'],)

    if transactions:
        transaction = transactions[0]
        linked_transactions.append(transaction)
        associ_trans = transaction.get('associated_transaction')

        if associ_trans:
            get_linked_transactions(associ_trans, linked_transactions)