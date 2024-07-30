from datetime import datetime
from frappe.utils.file_manager import remove_file
import frappe
import json

@frappe.whitelist(allow_guest=True)
def get_assignments_by_course(course_name="00"):
    try:
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Debug logging
        frappe.log_error(f"Fetching assignments for course: {course_name} as of {today}", "Assignment Fetch Debug")

        # Fetch assignments for the given course that are available to the student
        assignments = frappe.get_all(
            "LMS Assignment",
            fields=['name', 'assignment_title', 'to_date','assignment_type'],
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
    
    except Exception as e:
        # Detailed error logging
        frappe.log_error(f"Error fetching assignments: {str(e)}", "Assignment Fetch Error")
        frappe.response.update({
            "status_code": 500,
            "message": f"An error occurred while fetching assignments: {str(e)}"
        })
        
        return frappe.response["message"]

@frappe.whitelist(allow_guest=True)
def get_assignment(assignment_name="8e82ccda9e"):
    try:
        # Fetch the assignment document
        assignment_doc = frappe.get_doc("LMS Assignment", assignment_name)
        
        # Prepare the assignment details
        assignment = {
            "assignment_title": assignment_doc.assignment_title,
            "assignment_type":assignment_doc.assignment_type,
            "course": assignment_doc.course,
            "instruction": assignment_doc.instruction,
            "to_date": assignment_doc.to_date.strftime('%Y-%m-%d %H:%M:%S'),
            "question": assignment_doc.question,
            "total_grades": assignment_doc.total_grades,
            "attached_files": [],
            "assessment_criteria": []
        }

        # Fetch attached files from the 'attachment_file' field
        attached_files = frappe.get_all('File', filters={'attached_to_doctype': 'LMS Assignment', 'attached_to_name': assignment_name}, fields=['file_name', 'file_url'])

        for file in attached_files:
            assignment["attached_files"].append({
                "file_name": file['file_name'],
                "file_url": file['file_url']
            })

        # Fetch assessment criteria
        for criteria in assignment_doc.assessment_criteria:
            assignment["assessment_criteria"].append({
                "assessment_criteria": criteria.assessment_criteria,
                "maximum_grade": criteria.maximum_grade
            })

        # Check if the current user has submitted this assignment
        user_id = frappe.session.user
        student = frappe.get_value("Student", {"user_id": user_id}, "name")
        if student:
            submission = frappe.get_all('Assignment Submission', filters={
                'student': student,
                'assignment': assignment_name,
                'status': 'submitted'
            }, fields=['name'])
            is_submitted = bool(submission)
        else:
            is_submitted = False

        # Construct the success response
        frappe.response.update({
            "status_code": 200,
            "message": "Assignment details fetched successfully",
            "data": assignment,
            "is_submitted": is_submitted
        })
        return frappe.response["message"]

    except Exception as e:
        log_error("Assignment Fetch Error", f"An error occurred while fetching assignment details: {str(e)}")
        frappe.response.update({
            "status_code": 500,
            "message": f"An error occurred while fetching assignment details: {str(e)}"
        })
        return frappe.response["message"]

def log_error(title, message):
    try:
        if len(title) > 140:
            title = title[:140]
        frappe.log_error(message, title)
    except Exception as log_error:
        # Handle any errors that occur during logging to avoid infinite loop
        frappe.errprint(f"Error logging failed: {str(log_error)}")

@frappe.whitelist(allow_guest=True)
def create_assignment_submission():
    data = json.loads(frappe.request.data)

    user_id = frappe.session.user
    student = frappe.get_value("Student", {"user_id": user_id}, "name")
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

        if submit:
            submission_doc.status = "submitted"  # تحديث حالة التكليف إلى "submitted" عند الإرسال
        else:
            submission_doc.status = ""  # اترك الحقل فارغًا عند الحفظ فقط

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
            'submission_date': submission_date,
            'status': 'submitted' if submit else ''  # تعيين حالة التكليف إلى "submitted" عند الإرسال فقط
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

@frappe.whitelist()
def delete_attachment(file_url="/files/lms_assignment.json"):
    file_name = file_url.split("/")[-1]
    frappe.msgprint(f"Deleting file with URL: {file_url} and name: {file_name}")

    file_doc = frappe.get_all('File', filters={'file_url': file_url})
    frappe.msgprint(f"File Doc: {file_doc}")

    if file_doc:
        frappe.delete_doc('File', file_doc[0].name)
        frappe.msgprint(f"Deleted file from File doctype with name: {file_doc[0].name}")

        # البحث عن الوثيقة في دوك تايب Attachment Files
        attachment_file_doc = frappe.get_all('Attachment Files', filters={'attachment_file': file_url})
        frappe.msgprint(f"Attachment File Doc: {attachment_file_doc}")

        if attachment_file_doc:
            frappe.delete_doc('Attachment Files', attachment_file_doc[0].name)
            frappe.msgprint(f"Deleted file from Attachment Files with name: {attachment_file_doc[0].name}")

        frappe.db.commit()
        return {"status": "success", "message": "File deleted successfully from both File and Attachment Files"}
    else:
        frappe.msgprint("File not found in File doctype")
        return {"status": "error", "message": "File not found in File doctype"}

@frappe.whitelist(allow_guest=True)
def get_assignment_and_submission_details(assignment="ecff4b55c2"):
    user_id = frappe.session.user
    student = frappe.get_value("Student", {"user_id": user_id}, "name")
    
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

