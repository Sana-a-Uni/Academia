# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class StudentApplicant(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.admission.doctype.document.document import Document
		from academia.admission.doctype.qualification.qualification import Qualification
		from academia.admission.doctype.student_applicant_course_child.student_applicant_course_child import StudentApplicantCourseChild
		from frappe.types import DF

		academic_program: DF.Link
		address_line_1: DF.Data | None
		address_line_2: DF.Data | None
		application_status: DF.Literal["Applied", "Approved", "Rejected", "Admitted"]
		blood_group2: DF.Literal["", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
		blood_group: DF.Link | None
		city: DF.Data | None
		country: DF.Link | None
		date_of_birth2: DF.Date | None
		date_of_birth: DF.Link | None
		document: DF.Table[Document]
		faculty: DF.Link | None
		faculty_department: DF.Link | None
		first_name: DF.Data
		gender2: DF.Link | None
		gender: DF.Data | None
		guardians: DF.Text | None
		joining_date: DF.Date | None
		last_name: DF.Data | None
		middle_name: DF.Data | None
		naming_series: DF.Literal["ADM-SAP-.YYYY.-"]
		nationality2: DF.Data | None
		nationality: DF.Check
		program_degree: DF.Link | None
		qualification: DF.Table[Qualification]
		remedial_material: DF.Check
		remedial_materials: DF.Table[StudentApplicantCourseChild]
		state: DF.Data | None
		status: DF.Data | None
		student_email_address: DF.Data
		student_mobile_number2: DF.Data | None
		student_mobile_number: DF.Date
	# end: auto-generated types
		
@frappe.whitelist()
def select_data(condition_value):
    try:
        # Construct your SQL query
        sql_query = """
            select * from `tabRequirement Applicant Qualification Type` where parent = %s
        """
        # Execute the query
        data = frappe.db.sql(sql_query, (condition_value,), as_dict=True)
    
        # Return the fetched data
        return data
        
    except Exception as e:
        frappe.log_error(f"Error in selecting data: {str(e)}")
        return None
@frappe.whitelist()
def get_document(condition_value):
    try:
        # Construct your SQL query
        sql_query = """
            select * from `tabRequirement Applicant Document Type` where parent = %s
        """
        # Execute the query
        data = frappe.db.sql(sql_query, (condition_value,), as_dict=True)
    
        # Return the fetched data
        return data
        
    except Exception as e:
        frappe.log_error(f"Error in selecting data: {str(e)}")
        return None
	
	 
@frappe.whitelist()
def update_statues(condition_value,status):
	try:
		# Construct your SQL query
		sql_query = """
			update `tabStudent Applicant` set status = %s where name = %s
		"""
		# Execute the query
		data = frappe.db.sql(sql_query, (status,condition_value,), as_dict=True)
	
		# Return the fetched data
		return data
		
	except Exception as e:
		frappe.log_error(f"Error in selecting data: {str(e)}")
		return None

@frappe.whitelist()
def reject_student_application(docname, rejection_reason, email_subject, email_message):
    try:
        # Get the document
        doc = frappe.get_doc('Student Applicant', docname)
        doc.status = 'Rejected'
        doc.reject_reason = rejection_reason
        doc.save()

        # Get the student's email address
        recipient = doc.student_email_address
        if not recipient:
            frappe.throw(_("Student email address is not set for the applicant."))

        # Prepare the email message
        message = f"""
        Dear {doc.first_name},

        {email_message}

        Rejection Reason: {rejection_reason}

        Best Regards,
        Admissions Team
        """

        # Send the email
        frappe.sendmail(
            recipients=[recipient],
            subject=email_subject,
            message=message
        )
        return True
    except Exception as e:
        frappe.log_error(f"Error in rejecting student application: {str(e)}")
        return None