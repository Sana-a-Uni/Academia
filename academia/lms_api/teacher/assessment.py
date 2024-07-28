import frappe
import json
from frappe import _

def get_faculty_member_from_user(user_id):
    """
    Retrieve the faculty member ID linked to a user ID.

    :param user_id: The user ID to retrieve the faculty member for
    :return: The faculty member ID
    """
    employee_id = frappe.get_value("Employee", {"user_id": user_id}, "name")
    if not employee_id:
        raise frappe.ValidationError("Employee not found for the user.")
    
    faculty_member_id = frappe.get_value("Faculty Member", {"employee": employee_id}, "name")
    if not faculty_member_id:
        raise frappe.ValidationError("Faculty member not found for the employee.")
    
    return faculty_member_id

@frappe.whitelist(allow_guest=True)
def fetch_submitted_assignments_for_faculty_member():
    """
    Retrieve submitted assignments for the current faculty member.
    """
    user_id = frappe.session.user  # Get the current user ID from the session
    faculty_member_id = get_faculty_member_from_user(user_id)  # Retrieve faculty member ID
    if not faculty_member_id:
        raise frappe.ValidationError("Faculty member not found for the user.")
        
    submitted_assignments = frappe.db.sql("""
        SELECT
            student.name as student_name,
            assignment.assignment_title,
            assignment_submission.submission_date
        FROM
            `tabAssignment Submission` as assignment_submission
        JOIN
            `tabLMS Assignment` as assignment ON assignment_submission.assignment = assignment.name
        JOIN
            `tabStudent` as student ON assignment_submission.student = student.name
        WHERE
            assignment_submission.status = 'submitted'
            AND assignment.faculty_member = %s
        ORDER BY
            assignment_submission.submission_date DESC
    """, faculty_member_id, as_dict=True)

    frappe.response["status_code"] = 200
    frappe.response["submitted_assignments"] = submitted_assignments

@frappe.whitelist(allow_guest=True)
def fetch_assignment_details(assignment_submission_id):
    """
    Retrieve detailed information for a specific assignment submission.
    """
    if not assignment_submission_id:
        frappe.throw(_("Assignment Submission ID is required"))

    submission = frappe.get_doc('Assignment Submission', assignment_submission_id)
    assignment = frappe.get_doc('LMS Assignment', submission.assignment)
    student = frappe.get_doc('Student', submission.student)

    attached_files = frappe.get_all('File', filters={'attached_to_doctype': 'LMS Assignment', 'attached_to_name': assignment.name}, fields=['file_name', 'file_url'])
    student_files = frappe.get_all('File', filters={'attached_to_doctype': 'Assignment Submission', 'attached_to_name': submission.name}, fields=['file_name', 'file_url'])

    assessment_criteria = assignment.get('assessment_criteria', [])

    return {
        'question_text': assignment.question,
        'assignment_files': attached_files,
        'student_answer': submission.answer,
        'student_files': student_files,
        'comment': submission.comment,
        'assessment_criteria': assessment_criteria
    }

@frappe.whitelist(allow_guest=True)
def save_assignment_assessment():
    """
    Save an assessment for an assignment submission.
    """
    try:
        # Ensure the request is authenticated
        if frappe.session.user == "Guest":
            frappe.throw(_("You need to be logged in to access this resource."), frappe.AuthenticationError)
        
        data = json.loads(frappe.request.data)
        
        required_fields = ["assignment_submission", "feedback", "assessment_date", "criteria_grades"]
        for field in required_fields:
            if field not in data:
                frappe.throw(_("Missing required field: {0}").format(field))
        
        user_id = frappe.session.user  # Get the current user ID from the session
        faculty_member_id = get_faculty_member_from_user(user_id)  # Retrieve faculty member ID
        if not faculty_member_id:
            raise frappe.ValidationError("Faculty member not found for the user.")
        
        assessment = frappe.get_doc({
            "doctype": "Assignment Assessment",
            "assignment_submission": data["assignment_submission"],
            "faculty_member": faculty_member_id,
            "feedback": data["feedback"],
            "assessment_date": data["assessment_date"]
        })
        
        total_grade = 0
        for criteria_grade in data["criteria_grades"]:
            assessment_criteria_doc = frappe.get_doc("Assessment Criteria", criteria_grade["assessment_criteria"])
            grade = float(criteria_grade["grade"])
            total_grade += grade
            
            assessment.append("assignment_assessment_details", {
                "assessment_criteria": criteria_grade["assessment_criteria"],
                "grade": grade
            })
        
        assessment.grade = total_grade
        assessment.insert()
        
        try:
            # Update the status of the assignment submission to 'assessed' with ignore_permissions
            assignment_submission = frappe.get_doc("Assignment Submission", data["assignment_submission"])
            assignment_submission.db_set("status", "assessed", update_modified=True)
        except Exception as save_error:
            frappe.log_error(message=str(save_error), title="Update Assignment Submission Status Error")
            return {"status": "error", "message": _("Failed to update assignment submission status.")}
        
        frappe.db.commit()
        frappe.db.commit()
        
        return {"status": "success", "message": "Assessment saved successfully"}
    
    except frappe.AuthenticationError as e:
        frappe.log_error(message=str(e), title="Authentication Error")
        return {"status": "error", "message": _("Authentication failed. Please login to continue.")}
    
    except Exception as e:
        frappe.log_error(message=str(e), title="Save Assessment Error")
        return {"status": "error", "message": str(e)}