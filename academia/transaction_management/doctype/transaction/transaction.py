# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt


import frappe # type: ignore
from frappe.model.document import Document # type: ignore


class Transaction(Document):
    # pass
    def before_save(self):

        created_by = frappe.get_doc('User', frappe.session.user)
        self.created_by = created_by.name
    




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
def get_transaction_actions(transaction):
    transaction_actions = frappe.get_all('Transaction Action',
                                  filters={'main_transaction': transaction},
                                  fields=['*'],)
    return transaction_actions
  
@frappe.whitelist()
def get_transaction_category_requirement(transaction_category):
    requirements = frappe.get_all("Transaction Category  Requirement",
                                   filters={"parent": transaction_category},
                                    )
    return requirements