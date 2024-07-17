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

