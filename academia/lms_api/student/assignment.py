from typing import Dict, Any,List
from datetime import datetime
import frappe
import json

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



@frappe.whitelist(allow_guest=True)
def create_assignment_submission():
    data = json.loads(frappe.request.data)

    student = data.get('student')
    assignment = data.get('assignment')
    answer = data.get('answer')
    # attachment = data.get('attachment')  # Base64 encoded file content
    comment = data.get('comment')
    submit = data.get('submit')  # Boolean indicating if the submission is final

    if not student or not assignment or not answer:
        frappe.throw("Missing required parameters")

    submission_date = datetime.now()

    # Create new assignment submission
    submission_doc = frappe.get_doc({
        'doctype': 'Assignment Submission',
        'student': student,
        'assignment': assignment,
        'answer': answer,
        'comment': comment,
        'submission_date': submission_date
    })

    # if attachment:
    #     # Save the attachment file
    #     file_doc = frappe.get_doc({
    #         "doctype": "File",
    #         "file_name": f"{assignment}_{student}.pdf",  # You can change the file name and extension based on the actual file type
    #         "attached_to_doctype": "Assignment Submission",
    #         "attached_to_name": submission_doc.name,
    #         "content": attachment,
    #         "decode": True
    #     })
    #     file_doc.insert()
    #     submission_doc.attachment = file_doc.file_url

    submission_doc.insert()

    # Submit the document if `submit` is True
    if submit:
        submission_doc.submit()

    frappe.db.commit()

    # Return the name of the current assignment submission
    frappe.response["status_code"] = 200
    frappe.response["message"] = "Assignment saved successfully" if not submit else "Assignment submitted successfully"
    frappe.response["assignment_submission_id"] = submission_doc.name
