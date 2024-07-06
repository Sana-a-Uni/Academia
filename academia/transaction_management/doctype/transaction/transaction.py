# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt


from queue import Full
from jinja2 import Template # type: ignore
import os
import frappe # type: ignore
from frappe.model.document import Document # type: ignore
import json

class Transaction(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from academia.councils.doctype.topic_applicant.topic_applicant import TopicApplicant
        from academia.transaction_management.doctype.transaction_attachments.transaction_attachments import TransactionAttachments
        from academia.transaction_management.doctype.transaction_recipients.transaction_recipients import TransactionRecipients
        from frappe.types import DF

        amended_from: DF.Link | None
        applicants_table: DF.Table[TopicApplicant]
        attachments: DF.Table[TransactionAttachments]
        category: DF.Link | None
        company: DF.Link | None
        created_by: DF.Data | None
        department: DF.Link | None
        description: DF.TextEditor | None
        designation: DF.Link | None
        external_entity_designation_from: DF.Link | None
        external_entity_designation_to: DF.Link | None
        full_electronic: DF.Check
        main_external_entity_from: DF.Link | None
        main_external_entity_to: DF.Link | None
        print_official_paper: DF.Check
        priority: DF.Literal["", "Low", "Medium", "High", "Urgent"]
        private: DF.Check
        recipients: DF.Table[TransactionRecipients]
        reference_number: DF.Data | None
        referenced_doctype: DF.Link | None
        referenced_document: DF.DynamicLink | None
        start_date: DF.Data | None
        start_with: DF.Link | None
        start_with_company: DF.Link | None
        start_with_department: DF.Link | None
        start_with_designation: DF.Link | None
        status: DF.Literal["Pending", "Completed", "Canceled"]
        sub_category: DF.Link | None
        sub_external_entity_from: DF.Link | None
        sub_external_entity_to: DF.Link | None
        through_route: DF.Check
        title: DF.Data | None
        transaction_scan: DF.Attach | None
        transaction_scope: DF.Literal["In Company", "Among Companies", "With External Entity"]
        type: DF.Literal["Outgoing", "Incoming"]
    # end: auto-generated types
    def on_submit(self):
        if self.start_with:
            employee = frappe.get_doc("Employee", self.start_with)
            frappe.share.add(
                doctype = "Transaction",
                name = self.name,
                user = employee.user_id,
                read = 1,
                write = 0,
                share = 0
            )
        
        # make a read permission for applicants
        for row in self.applicants_table:
            applicant = frappe.get_doc(row.applicant_type, row.applicant)
            if row.applicant_type == "User":
                appicant_user_id = applicant.email
            else:
                appicant_user_id = applicant.user_id
            frappe.share.add(
				doctype = "Transaction",
				name = self.name,
				user = appicant_user_id,
				read = 1,
			)  
                    # check if the through_route is disabled
        if self.through_route == 1:
            employee = frappe.get_doc("Employee",
                                       self.start_with,
                                       fields=["reports_to"])
            share_permission_through_route(self, employee)             

        else:
            # make a read, write, share permissions for reciepents
            for row in self.recipients:
                # user = frappe.get_doc("User", row.recipient_email)
                frappe.share.add(
                        doctype = "Transaction",
                        name = self.name,
                        # user = user.email,
                        user = row.recipient_email,
                        read = 1,
                        write = 1,
                        share = 1
                    )
                 
    def before_save(self):
        if frappe.session.user != "Administrator":
            self.set_employee_details()

    def set_employee_details(self):
        # Fetch the current employee's document
        employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, ["department", "designation"], as_dict=True)
        if employee:
            self.department = employee.department
            self.designation = employee.designation  



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
def get_transaction_category_recipients(transaction_category):
    recipients = []

    # Fetch recipients for the selected transaction category
    transaction_category_recipients = frappe.get_all("Transaction Recipients",
                                                      filters={"parent": transaction_category},
                                                      fields=[
                                                          "recipient_name", 
                                                          "recipient_company", 
                                                          "recipient_department", 
                                                          "recipient_designation", 
                                                          "recipient_email"
                                                        ])
    recipients.extend(transaction_category_recipients)

    return recipients


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
    else:
        return None


@frappe.whitelist()
def get_user_permissions(docname, user):
    share = frappe.get_all("DocShare", filters={
        "share_doctype": "Transaction",
        "share_name": docname,
        "user": user
    }, fields=["read", "share", "submit", "write"], limit=1)

    if share:
        return share[0]
    else:
        return None

# def get_employee_by_user_id(user_id):
#     try:
#         # Check if an Employee document exists with the given user_id
#         employee = frappe.get_doc("Employee", {"user_id": user_id})
#         return employee
#     except frappe.DoesNotExistError:
#         # If no Employee document is found, return None
#         return None

@frappe.whitelist()
def get_employee_by_user_id(user_id):
    employee = frappe.get_all("Employee",
                            filters={"user_id": user_id},
                            fields=["name", "company", "designation", "department"])
    if employee:
        return employee[0]
    else:
        return None



@frappe.whitelist()
def create_new_transaction_action(user_id, transaction_name, type, details):
    """
    Create a new document in Transaction Action and pass the relevant data from Transaction.
    This function will be called when a button is pressed in Transaction.
    """
    transaction_doc = frappe.get_doc("Transaction", transaction_name)
    is_type = type in ["Approved", "Rejected"]
    is_through = transaction_doc.through_route

    if is_type and is_through:
        current_employee = frappe.get_all("Employee", filters={
                "user_id": user_id,
            }
              ,fields=["reports_to"]
            )
        next_share = frappe.get_doc("Employee", current_employee[0].reports_to)        
        is_reports_to = next_share != None
        is_report_not_recipient = next_share.user_id == transaction_doc.recipients[0].recipient_email

        if is_reports_to and is_report_not_recipient:
            share_permission_through_route(transaction_doc, current_employee[0])
    
    employee = get_employee_by_user_id(user_id)
    if employee:
        new_doc = frappe.new_doc("Transaction Action")
        new_doc.transaction = transaction_name
        new_doc.type = type
        new_doc.from_company = employee.company
        new_doc.from_department = employee.department
        new_doc.from_designation = employee.designation
        new_doc.details = details

        new_doc.submit()
        new_doc.save()

        if check_all_recipients_action(transaction_name, user_id):
            transaction_doc = frappe.get_doc("Transaction", transaction_name)
            transaction_doc.status = "Completed"
            transaction_doc.save()
        
        permissions = {
                            "read": 1,
                            "write": 0,
                            "share": 0,
                            "submit":0
                        }
        permissions_str = json.dumps(permissions)
        update_share_permissions(transaction_name, user_id, permissions_str)
        
        return "Action Success"
    else:
        return "No employee found for the given user ID."

def check_all_recipients_action(docname, user_id):
    shares = frappe.get_all("DocShare", filters={
                "share_doctype": "Transaction",
                "share_name": docname,
            }, fields=["share", "user"])
            
    for share in shares:
        if share["share"] == 1 and share["user"] != user_id:
            return False
            
    return True
                    

# to get html template 
@frappe.whitelist()
def get_actions_html(transaction_name):

        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        template_path = os.path.join(current_dir, "templates/vertical_path.html")

        # Load the template file
        with open(template_path, "r") as file:
            template_content = file.read()
        template = Template(template_content)

        recipient_actions = get_recipient_actions(transaction_name)
        # return recipient_actions
        context = {
            "recipient_actions": recipient_actions
        }
        
        # Render the template
        rendered_html = template.render(context)

        return rendered_html

def get_recipient_actions(transaction_name, action_name=''):
    parent = action_name if action_name != '' else transaction_name
    
    recipients = frappe.get_all("Transaction Recipients",
                                filters={"parent": parent},
                                fields=["recipient_email"],
                                order_by="creation"
                                )

    actions = frappe.get_all("Transaction Action",
                             filters={
                                 "transaction": transaction_name,
                                 "docstatus": 1,
                                 },
                             fields=["name", "type", "owner"],
                             order_by="creation"
                             )

    recipient_actions = []

    for recipient in recipients:
        recipient_dict = {
            "recipient": recipient.recipient_email,
            "action": None,
            "redirected": [],
            "link": None
        }

        for action in actions:
            if action.owner == recipient.recipient_email:
                recipient_dict["action"] = action
                recipient_dict["link"] = get_document_link("Transaction Action", action.name)
                if action.type == "Redirected":
                    redirected_recipients = get_recipient_actions(transaction_name, action.name)
                    recipient_dict["redirected"].append(redirected_recipients)

        recipient_actions.append(recipient_dict)

    return recipient_actions



def get_document_link(doctype, document_name):
    document = frappe.get_doc(doctype, document_name)
    link = document.get_url()
    return link


def share_permission_through_route(document, current_employee):
    reports_to = current_employee.reports_to
    if reports_to:
        reports_to_emp = frappe.get_doc("Employee", reports_to)
        # if reports_to_emp != document.recipients[0].recipient_email:
        frappe.share.add(
                    doctype = "Transaction",
                    name = document.name,
                    user = reports_to_emp.user_id,
                    read = 1,
                    write = 1,
                    share = 1
                )
    else:
        frappe.msgprint("Theres no any reports to")