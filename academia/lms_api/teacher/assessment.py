import frappe
import json
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_submitted_assignments_by_faculty_member(faculty_member_id= "ACAD-FM-00001"):
    if not faculty_member_id:
        frappe.throw(_("Faculty Member ID is required"))

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

    # إعداد الاستجابة
    frappe.response["status_code"] = 200
    frappe.response["submitted_assignments"] = submitted_assignments


@frappe.whitelist(allow_guest=True)
def get_assignment_details(assignment_submission_id="20817d93e8"):
    if not assignment_submission_id:
        frappe.throw(_("Assignment Submission ID is required"))

    submission = frappe.get_doc('Assignment Submission', assignment_submission_id)
    
    assignment = frappe.get_doc('LMS Assignment', submission.assignment)
    
    student = frappe.get_doc('Student', submission.student)

    attached_files = frappe.get_all('File', filters={'attached_to_doctype': 'LMS Assignment', 'attached_to_name': assignment.name}, fields=['file_name', 'file_url'])

    student_files = frappe.get_all('File', filters={'attached_to_doctype': 'Assignment Submission', 'attached_to_name': submission.name}, fields=['file_name', 'file_url'])

    assessment_criteria = []
    if hasattr(assignment, 'assessment_criteria'):
        assessment_criteria = assignment.get('assessment_criteria')

    return {
        'question_text': assignment.question,
        'assignment_files': attached_files,
        'student_answer': submission.answer,
        'student_files': student_files,
        'comment': submission.comment,
        'assessment_criteria': assessment_criteria
    }


@frappe.whitelist(allow_guest=True)
def save_assessment():
    try:
        data = json.loads(frappe.request.data)
        
        required_fields = ["assignment_submission", "faculty_member", "feedback", "assessment_date", "criteria_grades"]
        for field in required_fields:
            if field not in data:
                frappe.throw(_("Missing required field: {0}").format(field))
        
        assessment = frappe.get_doc({
            "doctype": "Assignment Assessment",
            "assignment_submission": data["assignment_submission"],
            "faculty_member": data["faculty_member"],
            "feedback": data["feedback"],
            "assessment_date": data["assessment_date"]
        })
        
        total_grade = 0
        for criteria_grade in data["criteria_grades"]:
            assessment_criteria_doc = frappe.get_doc("Assessment Criteria", criteria_grade["assessment_criteria"])
            
            frappe.log_error(message=f"Assessment Criteria Doc: {assessment_criteria_doc.as_dict()}", title="Criteria Debugging")
            
            grade = float(criteria_grade["grade"])
            total_grade += grade
            
            assessment.append("assignment_assessment_details", {
                "assessment_criteria": criteria_grade["assessment_criteria"],
                "grade": grade
            })
        
        assessment.grade = total_grade
        
        assessment.insert()
        frappe.db.commit()
        
        return {"status": "success", "message": "Assessment saved successfully"}
    
    except Exception as e:
        frappe.log_error(message=str(e), title="Save Assessment Error")
        return {"status": "error", "message": str(e)}
