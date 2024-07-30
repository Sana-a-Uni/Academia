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
            assignment_submission.name as assignment_submission_name,
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


from frappe.utils import getdate
from frappe.model.document import Document

@frappe.whitelist(allow_guest=True)
def save_assignment_assessment():
    """
    Save an assessment for an assignment submission.
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw(_("You need to be logged in to access this resource."), frappe.AuthenticationError)
        
        data = json.loads(frappe.request.data)
        
        required_fields = ["assignment_submission", "feedback", "assessment_date", "criteria_grades", "status"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            frappe.response["status_code"] = 400
            return {"status": "error", "message": _("Missing required fields: {0}").format(", ".join(missing_fields))}
        
        user_id = frappe.session.user
        faculty_member_id = get_faculty_member_from_user(user_id)
        if not faculty_member_id:
            frappe.response["status_code"] = 400
            return {"status": "error", "message": _("Faculty member not found for the user.")}
        
        docstatus = 0 if data["status"] == "draft" else 1
        
        # Check if there is an existing assessment for the given assignment_submission
        existing_assessment_name = frappe.get_value("Assignment Assessment", {"assignment_submission": data["assignment_submission"]}, "name")
        
        if existing_assessment_name:
            # Update the existing assessment
            assessment = frappe.get_doc("Assignment Assessment", existing_assessment_name)
            assessment.feedback = data["feedback"]
            assessment.assessment_date = getdate(data["assessment_date"])
            assessment.docstatus = docstatus
            
            # Clear existing criteria grades and re-add them
            assessment.set("assignment_assessment_details", [])
            total_grade = 0
            for criteria_grade in data["criteria_grades"]:
                grade = float(criteria_grade["grade"])
                
                if grade < 0:
                    frappe.response["status_code"] = 400
                    return {"status": "error", "message": _("Grade cannot be negative: {0}").format(grade)}
                
                max_grade = frappe.get_value("Assessment Criteria", criteria_grade["assessment_criteria"], "maximum_grade")
                if grade > max_grade:
                    frappe.response["status_code"] = 400
                    return {"status": "error", "message": _("Grade {0} exceeds the maximum allowed grade {1} for criteria {2}").format(grade, max_grade, criteria_grade["assessment_criteria"])}
                
                total_grade += grade
                
                assessment.append("assignment_assessment_details", {
                    "assessment_criteria": criteria_grade["assessment_criteria"],
                    "grade": grade
                })
            assessment.grade = total_grade
            assessment.save()
        else:
            # Create a new assessment
            assessment = frappe.get_doc({
                "doctype": "Assignment Assessment",
                "assignment_submission": data["assignment_submission"],
                "faculty_member": faculty_member_id,
                "feedback": data["feedback"],
                "assessment_date": getdate(data["assessment_date"]),
                "docstatus": docstatus
            })
            
            total_grade = 0
            for criteria_grade in data["criteria_grades"]:
                grade = float(criteria_grade["grade"])
                
                if grade < 0:
                    frappe.response["status_code"] = 400
                    return {"status": "error", "message": _("Grade cannot be negative: {0}").format(grade)}
                
                max_grade = frappe.get_value("Assessment Criteria", criteria_grade["assessment_criteria"], "maximum_grade")
                if grade > max_grade:
                    frappe.response["status_code"] = 400
                    return {"status": "error", "message": _("Grade {0} exceeds the maximum allowed grade {1} for criteria {2}").format(grade, max_grade, criteria_grade["assessment_criteria"])}
                
                total_grade += grade
                
                assessment.append("assignment_assessment_details", {
                    "assessment_criteria": criteria_grade["assessment_criteria"],
                    "grade": grade
                })
            assessment.grade = total_grade
            assessment.insert()
        
        if docstatus == 1:
            try:
                assignment_submission = frappe.get_doc("Assignment Submission", data["assignment_submission"])
                assignment_submission.db_set("status", "assessed", update_modified=True)
            except Exception as save_error:
                frappe.log_error(message=str(save_error), title="Update Assignment Submission Status Error")
                frappe.response["status_code"] = 500
                return {"status": "error", "message": _("Failed to update assignment submission status.")}
        
        frappe.db.commit()
        
        return {"status": "success", "message": "Assessment saved successfully"}
    
    except frappe.AuthenticationError as e:
        frappe.log_error(message=str(e), title="Authentication Error")
        frappe.response["status_code"] = 401
        return {"status": "error", "message": _("Authentication failed. Please login to continue.")}
    
    except Exception as e:
        frappe.log_error(message=str(e), title="Save Assessment Error")
        frappe.response["status_code"] = 500
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def get_assignment_assessment(assignment_submission_id):
    """
    Get the assessment details for a specific assignment submission.
    """
    try:
        assessment = frappe.get_all("Assignment Assessment", filters={"assignment_submission": assignment_submission_id}, fields=["*"])
        
        if assessment:
            assessment_doc = frappe.get_doc("Assignment Assessment", assessment[0].name)
            assessment_details = [detail.as_dict() for detail in assessment_doc.assignment_assessment_details]
            assessment[0]["assignment_assessment_details"] = assessment_details
            
            return {"status": "success", "data": assessment[0]}
        else:
            return {"status": "error", "message": _("No assessment found for the given assignment submission.")}
    
    except frappe.DoesNotExistError:
        return {"status": "error", "message": _("Assignment submission not found.")}
    except Exception as e:
        frappe.log_error(message=str(e), title="Get Assessment Error")
        return {"status": "error", "message": str(e)}
