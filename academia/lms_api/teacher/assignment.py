import frappe
import json
from typing import List, Dict, Any

@frappe.whitelist(allow_guest=True)
def get_assignments_by_course_and_faculty(course: str="00", faculty_member: str= "ACAD-FM-00001"):
    try:
        # Fetch all assignments that match the given course and faculty member
        assignments = frappe.get_all('LMS Assignment',
            filters={
                'course': course,
                'faculty_member': faculty_member
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
        # Create the assignment document
        create_assignment_doc(data)
    except Exception as e:
        frappe.response["status_code"] = 500
        frappe.response["message"] = f"An error occurred while creating the assignment: {str(e)}"
        return

    frappe.response["status_code"] = 200
    frappe.response["message"] = "Assignment created successfully"

def create_assignment_doc(data):
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
