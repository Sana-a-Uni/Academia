from typing import Dict, Any,List
from datetime import datetime
from frappe.utils.file_manager import remove_file
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
            "assignment_title": assignment_doc.assignment_title,
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
    comment = data.get('comment')
    attachments = data.get('attachments')  # List of dicts with 'attachment' (base64 content) and 'attachment_name'
    submit = data.get('submit')  # Boolean indicating if the submission is final

    if not student or not assignment or not answer:
        frappe.throw("Missing required parameters")

    existing_submission = frappe.get_all('Assignment Submission', filters={
        'student': student,
        'assignment': assignment
    }, fields=['name', 'docstatus'])

    submission_date = datetime.now()

    if existing_submission:
        submission_doc = frappe.get_doc('Assignment Submission', existing_submission[0]['name'])
        submission_doc.answer = answer
        submission_doc.comment = comment
        submission_doc.submission_date = submission_date

        if attachments:
            for attachment in attachments:
                attachment_content = attachment.get('attachment')
                attachment_name = attachment.get('attachment_name')
                if attachment_content and attachment_name:
                    file_doc = frappe.get_doc({
                        "doctype": "File",
                        "file_name": attachment_name,
                        "attached_to_doctype": "Assignment Submission",
                        "attached_to_name": submission_doc.name,
                        "content": attachment_content,
                        "decode": True
                    })
                    file_doc.insert()
                    submission_doc.append("attachment_files", {
                        "attachment_file": file_doc.file_url
                    })

        submission_doc.save()
        
        if submit and submission_doc.docstatus == 0:
            submission_doc.submit()
        else:
            submission_doc.save()

    else:
        submission_doc = frappe.get_doc({
            'doctype': 'Assignment Submission',
            'student': student,
            'assignment': assignment,
            'answer': answer,
            'comment': comment,
            'submission_date': submission_date
        })

        submission_doc.insert()

        if attachments:
            for attachment in attachments:
                attachment_content = attachment.get('attachment')
                attachment_name = attachment.get('attachment_name')
                if attachment_content and attachment_name:
                    file_doc = frappe.get_doc({
                        "doctype": "File",
                        "file_name": attachment_name,
                        "attached_to_doctype": "Assignment Submission",
                        "attached_to_name": submission_doc.name,
                        "content": attachment_content,
                        "decode": True
                    })
                    file_doc.insert()
                    submission_doc.append("attachment_files", {
                        "attachment_file": file_doc.file_url
                    })

        submission_doc.save()
        
        if submit:
            submission_doc.submit()

    frappe.db.commit()

    frappe.response["status_code"] = 200
    frappe.response["message"] = "Assignment saved successfully" if not submit else "Assignment submitted successfully"
    frappe.response["assignment_submission_id"] = submission_doc.name

@frappe.whitelist(allow_guest=True)
def get_assignment_and_submission_details(assignment="ecff4b55c2", student="EDU-STU-2024-00003"):
    # Fetch the submissions for the given assignment and student
    submissions = frappe.get_all('Assignment Submission', filters={'assignment': assignment, 'student': student}, fields=['name', 'answer', 'comment', 'submission_date'], order_by='submission_date desc')
    previous_submission = submissions[0] if submissions else None
    
    # Initialize the list for files
    files = []

    if previous_submission:
        # Fetch the attached files from the Attachment Files table
        attached_files = frappe.get_all('Attachment Files', filters={'parent': previous_submission['name'], 'parenttype': 'Assignment Submission'}, fields=['attachment_file'], order_by='creation desc')
        
        # Add files to the list
        for file in attached_files:
            files.append({
                "file_name": file.attachment_file.split('/')[-1],
                "file_url": file.attachment_file
            })

    # Set the response
    frappe.response["status_code"] = 200
    frappe.response["previous_submission"] = previous_submission
    frappe.response["files"] = files

@frappe.whitelist()
def delete_attachment(file_url):
    file_name = file_url.split("/")[-1]
    
    file_doc = frappe.get_all('File', filters={'file_name': file_name})
    
    if file_doc:
        frappe.delete_doc('File', file_doc[0].name)
        
        attachment_file_doc = frappe.get_all('Attachment Files', filters={'attachment_file': file_url})
        
        if attachment_file_doc:
            frappe.delete_doc('Attachment Files', attachment_file_doc[0].name)
        
        frappe.db.commit()
        return {"status": "success", "message": "File deleted successfully from both File and Attachment Files"}
    else:
        return {"status": "error", "message": "File not found in File doctype"}
