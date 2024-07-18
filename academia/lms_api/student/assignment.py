from typing import Dict, Any,List
from datetime import datetime
import frappe

@frappe.whitelist(allow_guest=True)
def get_assignments_by_course(course_name: str="00", student_id: str="EDU-STU-2024-00001") -> Dict[str, Any]:
    try:
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Fetch assignments for the given course that are available to the student
        assignments: List[Dict[str, Any]] = frappe.get_all(
            "LMS Assignment",
            fields=['name', 'assignment_title', 'to_date'],
            filters={
                'course': course_name,
                'make_the_assignment_availability': 1,
                'from_date': ['<=', today]
            },
            order_by='from_date asc'
        )

        # Construct the response
        frappe.response.update({
            "status_code": 200,
            "message": "Assignments fetched successfully",
            "data": assignments
        })
        
        return frappe.response["message"]
    
    # Construct the error response
    except Exception as e:
        frappe.response.update({
            "status_code": 500,
            "message": f"An error occurred while fetching assignments: {str(e)}"
        })
        
    return frappe.response["message"]


@frappe.whitelist(allow_guest=True)
def get_assignment(assignment_name: str="47dfd90592"):
    try:
        # Fetch the assignment document
        assignment_doc = frappe.get_doc("LMS Assignment", assignment_name)
        
        # Prepare the assignment details
        assignment = {
            "title": assignment_doc.assignment_title,
            "course": assignment_doc.course,
            "instruction": assignment_doc.instruction,
            "to_date": assignment_doc.to_date.strftime('%Y-%m-%d %H:%M:%S'),
            "question":assignment_doc.question,
            "total_grades": assignment_doc.total_grades,
            "attached_files": [],
            "assessment_criteria": []
        }

        # Fetch attached files and use a set to avoid duplicates
        attached_files_set = set()
        attached_files = frappe.get_all('File', filters={'attached_to_doctype': 'LMS Assignment', 'attached_to_name': assignment_name}, fields=['file_name', 'file_url'])
        for file in attached_files:
            file_tuple = (file.file_name, file.file_url)
            if file_tuple not in attached_files_set:
                attached_files_set.add(file_tuple)
                assignment["attached_files"].append({
                    "file_name": file.file_name,
                    "file_url": file.file_url
                })

        # Fetch assessment criteria
        for criteria in assignment_doc.assessment_criteria:
            assignment["assessment_criteria"].append({
                "assessment_criteria": criteria.assessment_criteria,
                "maximum_grade": criteria.maximum_grade
            })

        # Construct the success response
        frappe.response.update({
            "status_code": 200,
            "message": "Assignment details fetched successfully",
            "data": assignment
        })
        return frappe.response["message"]

    except Exception as e:
        # General error handling
        frappe.response.update({
            "status_code": 500,
            "message": f"An error occurred while fetching assignment details: {str(e)}"
        })
        return frappe.response["message"]
