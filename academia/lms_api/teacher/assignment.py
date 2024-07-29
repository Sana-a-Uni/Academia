import frappe
import json
from datetime import datetime

@frappe.whitelist(allow_guest=True)
def fetch_assignments_for_course(course):
    try:
        # Get the current user ID from the session
        user_id = frappe.session.user
        
        # Retrieve the faculty member ID linked to the user ID
        faculty_member_id = get_faculty_member_from_user(user_id)
        if not faculty_member_id:
            raise frappe.ValidationError("Faculty member not found for the user.")

        # Fetch all assignments that match the given course and faculty member
        assignments = frappe.get_all('LMS Assignment',
            filters={
                'course': course,
                'faculty_member': faculty_member_id
            },
            fields=['name', 'assignment_title', 'from_date', 'to_date', 'total_grades']
        )

        # Check if assignments were found
        if not assignments:
            frappe.response.update({
                "status_code": 404,
                "message": "No assignments found for the given course and faculty member."
            })
            return frappe.response["message"]

        # Construct the success response
        frappe.response.update({
            "status_code": 200,
            "message": "Assignments fetched successfully",
            "data": assignments
        })
        return frappe.response["message"]

    except Exception as e:
        # General error handling
        frappe.response.update({
            "status_code": 500,
            "message": f"An error occurred while fetching assignments: {str(e)}"
        })
        return frappe.response["message"]

@frappe.whitelist()
def create_assignment():
    data = json.loads(frappe.request.data)
    try:
        # Get the current user ID from the session
        user_id = frappe.session.user
        
        # Retrieve the faculty member ID linked to the user ID
        faculty_member_id = get_faculty_member_from_user(user_id)
        if not faculty_member_id:
            raise frappe.ValidationError("Faculty member not found for the user.")
        
        # Add the faculty member to the data dictionary
        data["faculty_member"] = faculty_member_id

        # Perform validation
        errors = validate_assignment_data(data)
        if errors:
            frappe.response["status_code"] = 400
            frappe.response["errors"] = errors
            return

        # Create the assignment document
        create_assignment_document(data)
    except Exception as e:
        frappe.response["status_code"] = 500
        frappe.response["message"] = f"An error occurred while creating the assignment: {str(e)}"
        return

    frappe.response["status_code"] = 200
    frappe.response["message"] = "Assignment created successfully"

def validate_assignment_data(data):
    errors = {}
    
    # Validate assignment title
    if not data.get("assignment_title"):
        errors["assignment_title"] = "Assignment title is required."
    
    # Validate question or attachment presence
    if not data.get("question") and not data.get("attachments"):
        errors["question_or_attachment"] = "Either question text or attachment is required."
    
    # Validate assessment criteria
    assessment_criteria_list = data.get("assessment_criteria")
    if not assessment_criteria_list or len(assessment_criteria_list) == 0:
        errors["assessment_criteria"] = "At least one assessment criteria is required."
    else:
        for index, criteria in enumerate(assessment_criteria_list):
            if not criteria.get("assessment_criteria"):
                if "assessment_criteria" not in errors:
                    errors["assessment_criteria"] = []
                errors["assessment_criteria"].append({ "index": index, "field": "assessment_criteria", "message": "Assessment criteria is required." })
            if not criteria.get("maximum_grade"):
                if "assessment_criteria" not in errors:
                    errors["assessment_criteria"] = []
                errors["assessment_criteria"].append({ "index": index, "field": "maximum_grade", "message": "Maximum grade is required." })
    
    # Validate dates if the assignment is available
    if data.get("make_the_assignment_availability") == 1:
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        if not from_date:
            errors["from_date"] = "From date is required when assignment availability is set."
        if not to_date:
            errors["to_date"] = "To date is required when assignment availability is set."
        if from_date and to_date:
            from_date_dt = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S')
            to_date_dt = datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S')
            if from_date_dt >= to_date_dt:
                errors["from_date"] = "From date must be earlier than To date."
            if from_date_dt <= datetime.now():
                errors["from_date"] = "From date must be in the future."
    
    return errors

def create_assignment_document(data):
    # Create the assignment document
    assignment_doc = frappe.new_doc("LMS Assignment")
    assignment_doc.course = data.get("course")
    assignment_doc.faculty_member = data.get("faculty_member")
    assignment_doc.assignment_title = data.get("assignment_title")
    assignment_doc.instruction = data.get("instruction")
    assignment_doc.make_the_assignment_availability = data.get("make_the_assignment_availability")

    if data.get("make_the_assignment_availability") == 1:
        assignment_doc.from_date = data.get("from_date")
        assignment_doc.to_date = data.get("to_date")

    assignment_doc.question = data.get("question")

    total_grades = 0
    assessment_criteria_list = data.get("assessment_criteria")
    if assessment_criteria_list:
        for criteria in assessment_criteria_list:
            criteria_row = assignment_doc.append("assessment_criteria", {})
            criteria_row.assessment_criteria = criteria.get("assessment_criteria")
            criteria_row.maximum_grade = criteria.get("maximum_grade")
            total_grades += criteria.get("maximum_grade", 0)

    assignment_doc.total_grades = total_grades

    # Insert the assignment document to get the name (ID) for attachments
    assignment_doc.insert()

    # Handling attachments
    attachments = data.get('attachments')
    if attachments:
        for attachment in attachments:
            attachment_content = attachment.get('attachment')
            attachment_name = attachment.get('attachment_name')
            if attachment_content and attachment_name:
                try:
                    file_doc = frappe.get_doc({
                        "doctype": "File",
                        "file_name": attachment_name,
                        "attached_to_doctype": "LMS Assignment",
                        "attached_to_name": assignment_doc.name,
                        "content": attachment_content,
                        "decode": True
                    })
                    file_doc.insert()
                    assignment_doc.append("attachment_file", {
                        "attachment_file": file_doc.file_url
                    })
                except Exception as e:
                    frappe.throw(f"Failed to upload attachment {attachment_name}: {str(e)}")

    # Save the document again to ensure attachments are linked
    assignment_doc.save()

def get_faculty_member_from_user(user_id):
    """
    Retrieve the faculty member linked to a user ID.

    :param user_id: The user ID to retrieve the faculty member for
    :return: The faculty member ID
    """
    # Get the employee ID linked to the user
    employee = frappe.get_value("Employee", {"user_id": user_id}, "name")
    if not employee:
        raise frappe.ValidationError("Employee not found for the user.")
    
    # Get the faculty member ID linked to the employee
    faculty_member = frappe.get_value("Faculty Member", {"employee": employee}, "name")
    if not faculty_member:
        raise frappe.ValidationError("Faculty member not found for the employee.")
    
    return faculty_member

