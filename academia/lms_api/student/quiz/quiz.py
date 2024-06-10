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
            fields=['name', 'title', 'to_date', 'is_time_bound', 'duration', 'number_of_attempts', 'total_grades'],
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
