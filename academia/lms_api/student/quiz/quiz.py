import frappe
from datetime import datetime
from typing import Dict, Any, List

@frappe.whitelist(allow_guest=True)
def get_quizzes_by_course(course_name: str , student_id: str ) -> Dict[str, Any]:
    try:
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Fetch quizzes for the given course that are available to the student
        quizzes: List[Dict[str, Any]] = frappe.get_all(
            "LMS Quiz",
            fields=['name', 'title', 'to_date',  'duration', 'number_of_attempts', 'total_grades'],
            filters={
                'course': course_name,
                'make_the_quiz_availability': 1,
                'from_date': ['<=', today]
            },
            order_by='from_date asc'
        )

        result_data = []

        for quiz in quizzes:
            # Fetch quiz results for the specific student
            quiz_results = frappe.get_all(
                "Quiz Result",
                fields=['grade', 'attempts_taken'],
                filters={
                    'quiz': quiz['name'],
                    'student': student_id
                }
            )

            # Update quiz information with results if available
            if quiz_results:
                quiz['grade'] = quiz_results[0]['grade']
                quiz['attempts_taken'] = quiz_results[0]['attempts_taken']
            else:
                quiz['grade'] = None
                quiz['attempts_taken'] = 0

            result_data.append(quiz)

        # Construct the response
        frappe.response.update({
            "status_code": 200,
            "message": "Quizzes fetched successfully",
            "data": result_data
        })
        
        return frappe.response["message"]
    
    # Construct the error response
    except Exception as e:
        frappe.response.update({
            "status_code": 500,
            "message": f"An error occurred while fetching quizzes: {str(e)}"
        })
        
        return frappe.response


@frappe.whitelist(allow_guest=True)
def get_quiz_instruction(quiz_name = "2874210861"):
    try:
        quiz_doc = frappe.get_doc("LMS Quiz", quiz_name)

        quiz_details = {
            "title": quiz_doc.title,
            "course": quiz_doc.course,
            "instruction": quiz_doc.instruction,
            "to_date": quiz_doc.to_date.strftime('%Y-%m-%d %H:%M:%S') if quiz_doc.make_the_quiz_availability else None,
            "duration": quiz_doc.duration if quiz_doc.is_time_bound else None,
            "max_attempts": quiz_doc.number_of_attempts,
            "grading_basis": quiz_doc.grading_basis,
            "total_grades": quiz_doc.total_grades
        }

        frappe.response.update({
            "status_code": 200,
            "message": "Quiz details fetched successfully",
            "data": quiz_details
        })
        return frappe.response["message"]

    except Exception as e:
        frappe.response.update({
            "status_code": 500,
            "message": "An error occurred while fetching quiz details."
        })
        return frappe.response["message"]

       