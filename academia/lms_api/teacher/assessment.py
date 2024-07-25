import frappe
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
