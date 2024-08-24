# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt


from queue import Full
from jinja2 import Template
import os
import frappe  # type: ignore
from frappe.model.document import Document  # type: ignore
import json
from datetime import datetime
from frappe import _

# from ..hijri_converter import convert_to_hijri


class Transaction(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from academia.transaction_management.doctype.transaction_applicant.transaction_applicant import TransactionApplicant
        from academia.transaction_management.doctype.transaction_attachments.transaction_attachments import TransactionAttachments
        from academia.transaction_management.doctype.transaction_recipients.transaction_recipients import TransactionRecipients
        from academia.transaction_management.doctype.transaction_signatories.transaction_signatories import TransactionSignatories
        from frappe.types import DF

        amended_from: DF.Link | None
        applicants_table: DF.Table[TransactionApplicant]
        attachments: DF.Table[TransactionAttachments]
        category: DF.Link | None
        circular: DF.Check
        company: DF.Link | None
        complete_time: DF.Datetime | None
        created_by: DF.Data | None
        department: DF.Link | None
        designation: DF.Link | None
        external_entity_designation_from: DF.Link | None
        external_entity_designation_to: DF.Link | None
        full_electronic: DF.Check
        hijri_date: DF.Data | None
        main_external_entity_from: DF.Link | None
        main_external_entity_to: DF.Link | None
        print_official_paper: DF.Check
        priority: DF.Literal["", "Low", "Medium", "High", "Urgent"]
        recipients: DF.Table[TransactionRecipients]
        reference_number: DF.Data | None
        reference_transaction: DF.Link | None
        referenced_doctype: DF.Link | None
        referenced_document: DF.DynamicLink | None
        signatories: DF.Table[TransactionSignatories]
        start_date: DF.Data | None
        start_from_employee: DF.Data | None
        start_with: DF.Link | None
        start_with_company: DF.Link | None
        start_with_department: DF.Link | None
        start_with_designation: DF.Link | None
        status: DF.Literal["Pending", "Completed", "Canceled", "Closed", "Rejected"]
        step: DF.Int
        sub_category: DF.Link | None
        sub_external_entity_from: DF.Link | None
        sub_external_entity_to: DF.Link | None
        submit_time: DF.Datetime | None
        through_route: DF.Check
        title: DF.Data
        transaction_description: DF.TextEditor | None
        transaction_scan: DF.Attach | None
        transaction_scope: DF.Literal["In Company", "Among Companies", "With External Entity"]
        type: DF.Literal["", "Outgoing", "Incoming"]
    # end: auto-generated types   

    def validate(self):
        # self.hijri_date=convert_to_hijri(self.start_date)
         # signatories
        signatories_employee = get_signatories(self)


        if len(signatories_employee) > 0:
            for emp in signatories_employee:
                
                signatory_field = self.append("signatories", {})
                signatory_field.official = emp.get("official")
                signatory_field.signatory_name = emp.get("name"),
                signatory_field.signatory_designation = emp.get("designation")

    def before_submit(self):
         # Save the current time as the last submitted time
        self.submit_time = datetime.now()

        # Check if there are any recipients in the child table
        if not self.recipients:
            raise ValueError("There must be at least one recipient to submit the transaction.")


    def on_submit(self):
        if self.start_with:
            employee = frappe.get_doc("Employee", self.start_with)
            frappe.share.add(
                doctype="Transaction",
                name=self.name,
                user=employee.user_id,
                read=1,
                write=0,
                share=0,
            )

        # make a read permission for applicants
        for row in self.applicants_table:
            applicant = frappe.get_doc(row.applicant_type, row.applicant)
            if row.applicant_type == "User":
                appicant_user_id = applicant.email
            else:
                appicant_user_id = applicant.user_id
            frappe.share.add(
                doctype="Transaction",
                name=self.name,
                user=appicant_user_id,
                read=1,
            )

        if self.through_route == 1:

            employee = frappe.get_doc(
                "Employee", self.start_with, fields=["reports_to", "user_id"]
            )
            share_permission_through_route(self, employee)

        elif self.transaction_scope == "Among Companies":

            company_head = frappe.get_doc("Transaction Company Head", {"company": self.start_with_company})
            head_employee_id = company_head.head_employee
            employee_user = frappe.get_doc("Employee", head_employee_id)
            user_id = employee_user.user_id
            recipients = [{
                "step": 1,
                "recipient_name": employee_user.employee_name,
                "recipient_company": employee_user.company,
                "recipient_department": employee_user.department,
                "recipient_designation": employee_user.designation,
                "recipient_email": user_id,
                "has_sign": 0,
                "print_paper": 0,
                "is_received": 0
            }]
            create_redirect_action(self.owner, self.name, recipients, self.step, 1)
            
            frappe.share.add(
                doctype="Transaction",
                name=self.name,
                user=user_id,
                read=1,
                write=1,
                share=1,
                submit=1,
            )
            frappe.db.commit()
        else:
            create_redirect_action(self.owner, self.name, self.recipients, self.step, 1)
            # make a read, write, share permissions for reciepents
            for row in self.recipients:
                if row.step == 1:
                    frappe.share.add(
                        doctype="Transaction",
                        name=self.name,
                        user=row.recipient_email,
                        read=1,
                        write=1,
                        share=1,
                        submit=1,
                    )
            frappe.db.commit()


        ###########################  

    def before_save(self):
        if frappe.session.user != "Administrator":
            self.set_employee_details()

        # to avoid "Value for Signatory Name cannot be a list" error
        self.set("signatories", [])        

    def set_employee_details(self):
        # Fetch the current employee's document
        employee = frappe.db.get_value(
            "Employee",
            {"user_id": frappe.session.user},
            ["department", "designation"],
            as_dict=True,
        )
        if employee:
            self.department = employee.department
            self.designation = employee.designation


def get_signatories(doc):
    signatories_employee = []

    if doc.start_with:

        start_with = frappe.get_doc("Employee",
                        doc.start_with,
                        fields=["employee_name", "designation"]
                        )
    
        signatories_employee.append({
            "name": start_with.employee_name,
            "designation": start_with.designation,
            "official": False
        })

        if doc.transaction_scope == "Among Companies":

            company_head = frappe.get_doc("Transaction Company Head", {"company": doc.start_with_company})
            if company_head:
                name = company_head.head_name
                designation = company_head.head_designation

            signatories_employee.append({
                "name": name,
                "designation": designation,
                "official": True
            })

        if doc.through_route:
            reports_to_list = get_reports_hierarchy_emp(doc.start_with)
            recipient_name = doc.recipients[0].recipient_name

            while reports_to_list:
                popped = reports_to_list.pop()
                if popped["name"] != recipient_name:
                    continue
                else:
                    break
            signatories_employee.extend(reports_to_list)
            # reports_to_list = get_reports_hierarchy_emp(doc.start_with)
            # reports_to_list.pop()
            # signatories_employee.extend(reports_to_list)

        if doc.sub_category:
            for recipient in doc.recipients:
                if recipient.has_sign:
                    signatories_employee.append({
                        "name": recipient.get("recipient_name"),
                        "designation": recipient.get("designation"),
                        "official": False
                    })
    return signatories_employee


def create_redirect_action(user, transaction_name, recipients, step=1, auto=0):
    employee = get_employee_by_user_id(user)

    new_doc = frappe.new_doc("Transaction Action")
    new_doc.transaction = transaction_name
    new_doc.type = "Redirected"

    for recipient in recipients:
        if recipient.get("step") == step:
            recipients_field = new_doc.append("recipients", {})
            recipients_field.step = recipient.get("step")
            recipients_field.recipient_name = recipient.get("recipient_name")
            recipients_field.recipient_company = recipient.get("recipient_company")
            recipients_field.recipient_department = recipient.get(
                "recipient_department"
            )
            recipients_field.recipient_designation = recipient.get(
                "recipient_designation"
            )
            recipients_field.recipient_email = recipient.get("recipient_email")
            recipients_field.has_sign = recipient.get("has_sign")
            recipients_field.print_paper = recipient.get("print_paper")
            recipients_field.is_received = recipient.get("is_received")
    if employee:
        new_doc.from_company = employee.company
        new_doc.from_department = employee.department
        new_doc.from_designation = employee.designation
    new_doc.auto_redirect = auto

    new_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    new_doc.save()

    new_doc.submit()


@frappe.whitelist()
def get_transaction_category_requirement(transaction_category):

    requirements = []

    # Fetch requirements for the selected transaction category
    transaction_category_requirements = frappe.get_all(
        "Transaction Category  Requirement",
        filters={"parent": transaction_category},
        fields=["name", "file_type", "required"],
    )
    requirements.extend(transaction_category_requirements)

    # Check if the transaction category has a parent category
    parent_category = frappe.db.get_value(
        "Transaction Category", transaction_category, "parent_category"
    )
    if parent_category:
        # Fetch requirements for the parent category
        parent_category_requirements = frappe.get_all(
            "Transaction Category  Requirement",
            filters={"parent": parent_category},
            fields=["name", "file_type", "required"],
        )
        requirements.extend(parent_category_requirements)


    return requirements


@frappe.whitelist()
def get_transaction_category_recipients(transaction_category):
    recipients = []

    # Fetch recipients for the selected transaction category
    transaction_category_recipients = frappe.get_all(
        "Transaction Recipients",
        filters={"parent": transaction_category},
        fields=[
            "step",
            "recipient_name",
            "recipient_company",
            "recipient_department",
            "recipient_designation",
            "recipient_email",
            "print_paper",
            "has_sign"
        ],
        order_by="step ASC",
    )
    recipients.extend(transaction_category_recipients)

    return recipients


@frappe.whitelist()
def update_share_permissions(docname, user, permissions):
    share = frappe.get_all(
        "DocShare",
        filters={"share_doctype": "Transaction", "share_name": docname, "user": user},
    )
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
    share = frappe.get_all(
        "DocShare",
        filters={"share_doctype": "Transaction", "share_name": docname, "user": user},
        fields=["read", "share", "submit", "write"],
        limit=1,
    )

    if share:
        return share[0]
    else:
        return None


@frappe.whitelist()
def get_employee_by_user_id(user_id):
    employee = frappe.get_all(
        "Employee",
        filters={"user_id": user_id},
        fields=["name", "company", "designation", "department"],
    )
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

    if transaction_doc.through_route:
        current_employee = frappe.get_all(
            "Employee",
            filters={
                "user_id": user_id,
            },
            fields=["user_id", "reports_to"],
        )
        share_permission_through_route(transaction_doc, current_employee[0])
    
    elif transaction_doc.transaction_scope == "Among Companies":
        company_head = frappe.get_doc("Transaction Company Head", {"company": transaction_doc.start_with_company})
        head_emp = frappe.get_doc("Employee", company_head.head_employee)
        if head_emp.user_id == user_id:
            end_recipient = transaction_doc.recipients[0]
            frappe.share.add(
                    doctype="Transaction",
                    name=transaction_doc.name,
                    user=end_recipient.recipient_email,
                    read=1,
                    write=1,
                    share=1,
                    submit=1,
                )
            recipient = {
                "step": 1,
                "recipient_name": end_recipient.recipient_name,
                "recipient_company": end_recipient.recipient_company,
                "recipient_department": end_recipient.recipient_department,
                "recipient_designation": end_recipient.recipient_designation,
                "recipient_email": end_recipient.recipient_email,
            }
            recipients = [recipient]

            create_redirect_action(
                user=user_id,
                transaction_name=transaction_doc.name,
                recipients=recipients,
                step=1,
                auto=1,
            )

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

        check_result = check_all_recipients_action(transaction_name, user_id)

        if check_result:
            transaction_doc = frappe.get_doc("Transaction", transaction_name)

            next_step = transaction_doc.step + 1
            next_step_recipients = frappe.get_all(
                "Transaction Recipients",
                filters={"parent": transaction_doc.name, "step": ("=", next_step)},
                fields=["recipient_email", "step"],
            )
            if len(next_step_recipients) > 0:
                for recipient in next_step_recipients:
                    frappe.share.add(
                        doctype="Transaction",
                        name=transaction_doc.name,
                        user=recipient.recipient_email,
                        read=1,
                        write=1,
                        share=1,
                        submit=1,
                    )
                transaction_doc.step = next_step
            else:
                transaction_doc.status = "Completed"
                transaction_doc.complete_time = datetime.now()

            transaction_doc.save()
        permissions = {"read": 1, "write": 0, "share": 0, "submit": 0}
        permissions_str = json.dumps(permissions)
        update_share_permissions(transaction_name, user_id, permissions_str)

        return "Action Success"
    else:
        return "No employee found for the given user ID."

@frappe.whitelist()
def check_all_recipients_action(docname, user_id):
    shares = frappe.get_all(
        "DocShare",
        filters={
            "share_doctype": "Transaction",
            "share_name": docname,
            "share": 1,
        },
        fields=["user"],
    )

    return_result = True

    for share in shares:
        if share["user"] != user_id:
            return_result = False

    return return_result


# to get html template
@frappe.whitelist()
def get_actions_html(transaction_name):
    current_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
    template_path = os.path.join(
        current_dir, "transaction_management/templates/vertical_path.html"
    )

    # Load the template file
    with open(template_path, "r") as file:
        template_content = file.read()
    template = Template(template_content)

    recipient_actions = json.loads(get_actions(transaction_name))
    # return recipient_actions
    context = {"recipient_actions": recipient_actions}

    # Render the template
    rendered_html = template.render(context)

    return rendered_html


@frappe.whitelist()
def get_actions(transaction_name):
    actions = frappe.get_all(
        "Transaction Action",
        filters={
            "transaction": transaction_name,
            "docstatus": 1,
        },
        fields=["name", "type", "owner", "auto_redirect"],
        order_by="creation",
    )

    recipients = []
    i = 0
    while i < len(actions):
        action = actions[i]

        if action.auto_redirect == 1:
            new_recipients = frappe.get_all(
                "Transaction Recipients",
                filters={"parent": action.name},
                fields=["recipient_email"],
                order_by="creation",
            )
            recipients.extend(new_recipients)
            del actions[i]
        else:
            i += 1
    recipient_actions = get_actions_recursion(actions, recipients)

    return json.dumps(recipient_actions)
    # return recipient_actions


def get_actions_recursion(actions, recipients=[], processed_recipients=None):
    if processed_recipients is None:
        processed_recipients = set()

    recipient_actions = []
    recipient = None

    for recipient in recipients:
        if recipient.recipient_email in processed_recipients:
            continue

        processed_recipients.add(recipient.recipient_email)

        recipient_dict = {
            "recipient": recipient.recipient_email,
            "action": None,
            "redirected": [],
            "link": None,
        }

        for action in actions:
            if action.owner == recipient.recipient_email and action.auto_redirect == 0:
                recipient_dict["action"] = action
                recipient_dict["link"] = get_document_link(
                    "Transaction Action", action.name
                )
                if action.type == "Redirected":
                    redirected_recipients = frappe.get_all(
                        "Transaction Recipients",
                        filters={"parent": action.name},
                        fields=["recipient_email"],
                        order_by="creation",
                    )
                    redirected_recipients = [
                        r
                        for r in redirected_recipients
                        if r.recipient_email not in processed_recipients
                    ]
                    recipient_dict["redirected"] = get_actions_recursion(
                        actions, redirected_recipients, processed_recipients
                    )

        recipient_actions.append(recipient_dict)

    return recipient_actions


def get_document_link(doctype, document_name):
    document = frappe.get_doc(doctype, document_name)
    link = document.get_url()
    return link


def share_permission_through_route(document, current_employee):
    
    reports_to = current_employee.reports_to
    if document.transaction_scope == "Among Companies":
        company_head = frappe.get_doc("Transaction Company Head", {"company": document.start_with_company})
        head_emp = frappe.get_doc("Employee", company_head.head_employee)
        if head_emp.user_id == current_employee.user_id:
            end_recipient = document.recipients[0]
            frappe.share.add(
                    doctype="Transaction",
                    name=document.name,
                    user=end_recipient.recipient_email,
                    read=1,
                    write=1,
                    share=1,
                    submit=1,
                )
            recipient = {
                "step": 1,
                "recipient_name": end_recipient.recipient_name,
                "recipient_company": end_recipient.recipient_company,
                "recipient_department": end_recipient.recipient_department,
                "recipient_designation": end_recipient.recipient_designation,
                "recipient_email": end_recipient.recipient_email,
            }
            recipients = [recipient]

            create_redirect_action(
                user=current_employee.user_id,
                transaction_name=document.name,
                recipients=recipients,
                step=1,
                auto=1,
            )
            return

    if current_employee.user_id != document.recipients[0].recipient_email:

        reports_to_emp = frappe.get_doc("Employee", reports_to)
        # if reports_to_emp != document.recipients[0].recipient_email:
        frappe.share.add(
            doctype="Transaction",
            name=document.name,
            user=reports_to_emp.user_id,
            read=1,
            write=1,
            share=1,
            submit=1,
        )

        recipient = {
            "step": 1,
            "recipient_name": reports_to_emp.employee_name,
            "recipient_company": reports_to_emp.company,
            "recipient_department": reports_to_emp.department,
            "recipient_designation": reports_to_emp.designation,
            "recipient_email": reports_to_emp.user_id,
        }
        recipients = [recipient]

        create_redirect_action(
            user=current_employee.user_id,
            transaction_name=document.name,
            recipients=recipients,
            step=1,
            auto=1,
        )

@frappe.whitelist()
def get_category_doctype(sub_category):
    """
    Fetches the template_doctype from the Transaction Category Template
    and sets it as the referenced_doctype in the current Transaction document.
    """
    if sub_category:
        category_doc = frappe.get_doc("Transaction Category", sub_category)
        if category_doc.template:
            template_doc = frappe.get_doc(
                "Transaction Category Template", category_doc.template
            )
            return template_doc.template_doctype
    return ""


@frappe.whitelist()
def get_template_description(sub_category):
    if sub_category:
        category_doc = frappe.get_doc("Transaction Category", sub_category)
        if category_doc.template:
            template_doc = frappe.get_doc(
                "Transaction Category Template", category_doc.template
            )
            return template_doc.description
    return ""


@frappe.whitelist()
def render_template(referenced_doctype, referenced_document, sub_category):
    if referenced_doctype and referenced_document and sub_category:
        try:
            template_description = get_template_description(sub_category)

            if template_description:
                doc = frappe.get_doc(referenced_doctype, referenced_document)

                linked_field_values = get_linked_field_values(
                    sub_category, referenced_document
                )
                context = doc.as_dict()

                if linked_field_values:
                    context.update(
                        {
                            item["docfield_title"]: item["value"]
                            for item in linked_field_values
                        }
                    )
                    template = Template(template_description)
                    return template.render(context)
                else:
                    template = Template(template_description)
                    return template.render(context)

            else:
                frappe.log_error(
                    f"Error fetching template description for sub_category: {sub_category}"
                )
                return None
        except frappe.DoesNotExistError:
            frappe.log_error(
                f"Error rendering template for {referenced_doctype}: {referenced_document}"
            )
            return None
    else:
        return None


@frappe.whitelist()
def get_linked_field_values(sub_category, referenced_document):
    """
    Fetches the linked field values from the Transaction based on the provided sub_category.
    """
    if sub_category:
        category_doc = frappe.get_doc("Transaction Category", sub_category)
        if category_doc.template:
            template_doc = frappe.get_doc(
                "Transaction Category Template", category_doc.template
            )
            template_doctype = template_doc.template_doctype
            linked_fields = template_doc.get("linked_fields", [])

            if linked_fields:
                field_values = []
                for field in linked_fields:
                    value = frappe.db.get_value(
                        template_doctype, referenced_document, field.link_field
                    )
                    if value:
                        field_values.append(
                            {
                                "link_field": field.link_field,
                                "doctype_name": field.doctype_name,
                                "docfield_name": field.docfield_name,
                                "docfield_title": field.docfield_title,
                                "value": value,
                            }
                        )

                jinja_values = []
                for item in field_values:
                    record = frappe.get_doc(item["doctype_name"], item["value"])
                    jinja_value = getattr(record, item["docfield_name"])
                    jinja_values.append(
                        {"docfield_title": item["docfield_title"], "value": jinja_value}
                    )

                return jinja_values

            return []
    return []

# to get recipients for bottom up states
@frappe.whitelist()
def get_reports_hierarchy(employee_name):
    reports_emails = []
    employee = frappe.get_doc("Employee", employee_name)
    reports_to = employee.reports_to

    while reports_to:
        employee = frappe.get_doc("Employee", reports_to)
        reports_emails.append(employee.user_id)
        reports_to = employee.reports_to

    return reports_emails

# to get recipients from top down states
@frappe.whitelist()
def get_reports_hierarchy_reverse(employee_name):
    employees = []
    
    # Get employees with reports_to set as the given employee
    direct_reports = frappe.get_all(
        "Employee",
        filters={"reports_to": employee_name},
        fields=["user_id", "name"]
    )

    
    # Iterate over direct reports
    for employee in direct_reports:
        # frappe.msgprint(f"{employee.user_id}")
        employees.append(employee.user_id)
        
        # Recursively call the function for each direct report
        employees += get_reports_hierarchy_reverse(employee.name)
    
    return employees

def get_reports_hierarchy_emp(employee_name):
    reports_employee = []
    employee = frappe.get_doc("Employee", employee_name)
    reports_to = employee.reports_to

    while reports_to:
        employee = frappe.get_doc("Employee", reports_to)
        reports_employee.append({
                "name": employee.employee_name,
                "designation": employee.designation,
                "official": False
            })
        reports_to = employee.reports_to

    return reports_employee



@frappe.whitelist()
def update_closed_premissions(docname):
    
    docshares = frappe.get_all(
        "DocShare",
        filters={"share_doctype": "Transaction", "share_name": docname,},
    )
    share_user = []
    if docshares:
        for docsh in docshares:
            docshare = frappe.get_doc("DocShare", docsh.name)
            # share_user.append(docshare.user)
            share_user = docshare.user

            permissions = {"read": 1, "write": 0, "share": 0, "submit": 0}
            permissions_str = json.dumps(permissions)
            update_share_permissions(docname, share_user, permissions_str)

        # Update the status of the transaction to "Closed"
        transaction = frappe.get_doc("Transaction", docname)
        transaction.status = "Closed"
        transaction.save()
    
        return "Closed successfully"
    
    else:
        # Update the status of the transaction to "Closed"
        transaction = frappe.get_doc("Transaction", docname)
        transaction.status = "Closed"
        transaction.save()
        return "There are no share users"


@frappe.whitelist()
def search_in_actions_for_print_paper_user(transacion_name, user, from_company, from_department, from_designation):
    actions = frappe.get_all(
        "Transaction Action",
        filters={"transaction": transacion_name, 
                 "type": "Redirected",
                 "from_company": from_company,
                 "from_department": from_department,
                 "from_designation": from_designation,
                },
        fields=["name"],
        order_by="creation desc"
    )

    for action in actions:
        recipients = frappe.get_all(
            "Transaction Recipients",
            filters={
                "parent": action.name,
                "recipient_email": user,
            },
            fields=["name", "print_paper", "is_received"],
        )
        if recipients:
            return action.name, recipients[0].print_paper, recipients[0].is_received, recipients[0].name
        
    return actions


@frappe.whitelist()
def change_is_received_in_action_recipients(rcipient_name):
    action = frappe.get_doc("Transaction Recipients", rcipient_name)
    

    action.is_received = 1
    action.save(ignore_permissions=True)


    return action


@frappe.whitelist()
def create_transaction(priority,title, category, sub_category,refrenced_document,applicants_list ):
    if(is_parent_category(category, sub_category)):
            # frappe.msgprint("ttttttt")
            pass

        
            template=get_template_by_category(sub_category)
            #main
            new_transaction = frappe.new_doc("Transaction")
            new_transaction.transaction_scope = "In Company"
            new_transaction.start_date =  datetime.now()
            new_transaction.hijri_date =  ""#??
            new_transaction.priority = priority
            new_transaction.status = "Pending"
            new_transaction.submit_time = datetime.now()
            new_transaction.title = title
            new_transaction.transaction_description =template.description
            new_transaction.category = category
            new_transaction.sub_category = sub_category
            new_transaction.referenced_doctype = template.template_doctype
            new_transaction.referenced_document = refrenced_document

            #from-- empty
            

            #creator-- no need

            # Add attachments to the transaction
            # for attachment_data in attachments:
            #     attachment = frappe.new_doc("Attachment")
            #     attachment.file_url = attachment_data.get("file_url")
            #     attachment.file_name = attachment_data.get("file_name")
            #     attachment.file_size = attachment_data.get("file_size")
            #     new_transaction.append("attachments", attachment)


            # Save the document
            frappe.msgprint("inserted") 

            # Call create_applicants to add applicants to the transaction
            frappe.msgprint(applicants_list)
            new_transaction.insert(ignore_permissions=True)

            # frappe.msgprint(new_transaction)
            if(applicants_list):
                create_applicants(new_transaction, applicants_list)

            # create_attachements(new_transaction, attachements_list)
            # create_attachements(new_transaction,sub_category,attachements_list)

        
        


        
            return new_transaction.name



def is_parent_category(category_name, sub_category_name):
    # Get the parent category document
    parent_category = frappe.get_doc("Transaction Category", {"category_name": category_name})
    
    # Get the sub-category document
    sub_category = frappe.get_doc("Transaction Category", {"category_name": sub_category_name})
    
    # Check if the sub-category's parent category is equal to the provided parent category
    if sub_category.parent_category == parent_category.name:
        return True
    else:
        return False
    

def get_template_by_category(category_name):
    
    # Get the Category document based on category_name
    category = frappe.get_doc("Transaction Category", category_name)
    # frappe.msgprint(category)
    
    # # Get the Template linked to the Category
    template = frappe.get_doc("Transaction Category Template", category.template)
    
    
    return template


def create_applicants( transaction_doc,applicants_list):
    applicants_list = json.loads(applicants_list)
    print(applicants_list)
    for applicant_data in applicants_list:
            frappe.msgprint("--------------------------------------")
        
            applicant = frappe.new_doc("Transaction Applicant")
            applicant.applicant_type = applicant_data["applicant_type"]
            applicant.applicant = applicant_data["applicant"]
            applicant.applicant_name = applicant_data["applicant_name"]
            # applicant.parent = transaction_doc

            
            
            # # Link the applicant to the transaction
            transaction_doc.append("applicants_table", {
                "applicant_type": applicant.applicant_type,
                "applicant": applicant.applicant,
                "applicant_name": applicant.applicant_name
            })

            
          
    
        
    transaction_doc.save()
    # frappe.db.commit()




def create_attachements( transaction_doc,sub_category,attachements_list):
    attachements_list = json.loads(attachements_list)

    requirements=get_transaction_category_requirement(sub_category)
    requirements_str = ', '.join(map(str, requirements))
    frappe.msgprint("requirements:"+requirements_str)
    
     # frappe.msgprint(requirements)
    for requirement_data in requirements:
        requirement=frappe.new_doc("Transaction Attachments")
        requirement.attachment_label=requirement_data["name"]
        requirement.required=requirement_data["required"]
    # Link the applicant to the transaction
        transaction_doc.append("attachments", {
                "attachment_label": requirement.attachment_label,
                "required": requirement.required,
               
            })
        transaction_doc.save()    



            
            


@frappe.whitelist()
def set_company_head(user_id, company_of_creator):
    # should to delete this after fix through route problem
    if(user_id == "Administrator"):
        employee = True
        company = company_of_creator
    else:
        employee = get_employee_by_user_id(user_id)
        company = employee.company
   
    if(employee):
        head = frappe.get_doc("Transaction Company Head", {"company": company})
        if(head):
            return head 
    return f"No Head for {company}"


@frappe.whitelist()
def get_all_employees_except_start_with_company(start_with_company):
    employees = frappe.get_list("Employee", filters={"company": ["!=", start_with_company]}, fields=["user_id"])
    return [emp.user_id for emp in employees]


@frappe.whitelist()
def is_there_approve_or_reject_acions(docname):
    actions = frappe.get_all(
        "Transaction Action", 
        filters={"transaction":docname, "docstatus": 1, "type": not "Canceled"}, 
        fields=["name", "transaction", "type", "owner"],
    )
    if actions:
        for action in actions:
            if action.type == "Approved" or action.type == "Rejected":
                return True

@frappe.whitelist()
def redirect_in_coming_among_companies(recipients):
    pass


   
@frappe.whitelist()
def create_new_topic(docname, user):
    employee = get_employee_by_user_id(user)

    new_doc = frappe.new_doc("Transaction Action")
    new_doc.transaction = docname
    new_doc.type = "Topic"

    if employee:
        new_doc.from_company = employee.company
        new_doc.from_department = employee.department
        new_doc.from_designation = employee.designation
    
    new_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    new_doc.save()

    # Call the create_topic_from_transaction function from the other module
    from academia.councils.doctype.topic.topic import create_topic_from_transaction
    create_topic_from_transaction(docname, new_doc.name, None)

    new_doc.submit()

@frappe.whitelist()
def get_last_topic_action(docname):
    actions = frappe.get_all(
        "Transaction Action",
        filters={
            "transaction": docname,
            "docstatus": 1,
            "type": "Topic",
        },
        fields=["name", "type", "topic_status"],
    )   

    if actions[0].topic_status == "Complete":
        return True
         
    return False
          
   