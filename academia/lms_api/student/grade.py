import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_quiz_and_assignment_grades(course):
    user_id = frappe.session.user
    
    student = frappe.get_value("Student", {"user_id": user_id}, "name")
    if not student:
        return {"error": "Student not found"}
    
    frappe.logger().info(f"Student: {student}, Course: {course}")

    quizzes = frappe.db.sql("""
        SELECT
            q.title AS title,
            q.name AS name,                
            qr.grade AS grade,
            q.total_grades AS total_grades,
            'quiz' AS type
        FROM
            `tabLMS Quiz` q
        JOIN
            `tabQuiz Result` qr ON q.name = qr.quiz
        WHERE
            qr.student = %s AND q.course = %s
    """, (student, course), as_dict=True)
    
    frappe.logger().info(f"Quizzes: {quizzes}")

    assignments = frappe.db.sql("""
        SELECT
            a.assignment_title AS title,
            a.name AS name,
            aa.grade AS grade,
            a.total_grades AS total_grades,
            'assignment' AS type
        FROM
            `tabLMS Assignment` a
        JOIN
            `tabAssignment Assessment` aa ON a.name = aa.assignment
        WHERE
            aa.student = %s AND a.course = %s
    """, (student, course), as_dict=True)
    
    frappe.logger().info(f"Assignments: {assignments}")

    results = {
        "quizzes": quizzes,
        "assignments": assignments
    }

    return results

@frappe.whitelist(allow_guest=True)
def get_quiz_attempts(quiz_name):
    user_id = frappe.session.user
    student = frappe.get_value("Student", {"user_id": user_id}, "name")

    if not student:
        return {"status": "error", "message": "Student not found"}

    attempts_data = frappe.db.sql("""
        SELECT
            qa.start_time,
            qa.end_time,
            qa.time_taken,
            qa.grade AS attempt_grade,
            lq.total_grades,
            lq.show_correct_answer,
            lq.grading_basis,
            lq.to_date,
            lq.title,
            rq.grade AS result_grade
        FROM
            `tabQuiz Attempt` qa
        JOIN
            `tabLMS Quiz` lq ON qa.quiz = lq.name
        LEFT JOIN
            `tabQuiz Result` rq ON qa.name = rq.name
        WHERE
            qa.quiz = %s AND qa.student = %s
    """, (quiz_name, student), as_dict=True)

    if not attempts_data:
        return {"status": "error", "message": "No attempts found"}

    attempts = []
    for attempt in attempts_data:
        attempt_info = {
            "start_time": attempt["start_time"],
            "end_time": attempt["end_time"],
            "time_taken": attempt["time_taken"],
            "attempt_grade": attempt["attempt_grade"],
            "show_correct_answer": attempt["show_correct_answer"]
        }
        quiz_details= {
            "total_grades": attempt["total_grades"],
            "grading_basis": attempt["grading_basis"],
            "to_date": attempt["to_date"],
            "title": attempt["title"],
            "result_grade": attempt["result_grade"]
        }
        attempts.append({"quizDetails": quiz_details, "attempts": attempt_info})

    return attempts


@frappe.whitelist(allow_guest=True)
def get_assignment_assessment_details(assignment_name):
    user_id = frappe.session.user
    if user_id == "Guest":
        frappe.throw("You must be logged in to access this information")

    student = frappe.get_value("Student", {"user_id": user_id}, "name")
    if not student:
        frappe.throw("Student record not found")

    assignment_assessment = frappe.db.sql("""
        SELECT
            aa.grade AS assignment_grade,
            aa.feedback
        FROM
            `tabAssignment Assessment` aa
        WHERE
            aa.assignment = %s AND aa.student = %s
    """, (assignment_name, student), as_dict=True)

    if not assignment_assessment:
        return {
            "assignment_grade": None,
            "feedback": None,
            "assessment_details": []
        }

    assessment_details = frappe.db.sql("""
        SELECT
            aad.assessment_criteria,
            ac.maximum_grade,
            ac.assessment_criteria AS criteria_text,
            aad.grade AS criteria_grade
        FROM
            `tabAssignment Assessment Details` aad
        JOIN
            `tabAssignment Assessment` aa ON aa.name = aad.parent
        JOIN
            `tabAssessment Criteria` ac ON ac.name = aad.assessment_criteria
        WHERE
            aa.assignment = %s AND aa.student = %s
    """, (assignment_name, student), as_dict=True)

    assignment_details = frappe.db.get_value("LMS Assignment", assignment_name, ["assignment_title", "assignment_type", "to_date", "total_grades"], as_dict=True)

    result = {
        "assignment_grade": assignment_assessment[0].get("assignment_grade"),
        "feedback": assignment_assessment[0].get("feedback"),
        "assessment_details": assessment_details or [],
        "assignment_info": assignment_details
    }

    return result
