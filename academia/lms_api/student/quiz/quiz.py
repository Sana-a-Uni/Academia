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
        
    return frappe.response["message"]


@frappe.whitelist(allow_guest=True)
def get_quiz_instruction(quiz_name: str, student_id: str ) -> Dict[str, Any]:
    try:
        quiz_doc = frappe.get_doc("LMS Quiz", quiz_name)

        # Check if the quiz is no longer available
        if not quiz_doc.make_the_quiz_availability or (quiz_doc.to_date < datetime.now()):
            frappe.response.update({
                "status_code": 403,
                "message": "This quiz is no longer available."
            })
            return frappe.response["message"]
        
       # Check the number of attempts left for the student
        quiz_results = frappe.get_all('Quiz Result', filters={'student': student_id, 'quiz': quiz_name}, fields=['attempts_taken'])
        current_attempts = quiz_results[0]['attempts_taken'] if quiz_results else 0
        attempts_left = quiz_doc.number_of_attempts - current_attempts

        # Check if the student has reached the maximum number of attempts
        if current_attempts >= quiz_doc.number_of_attempts:
            frappe.response.update({
                "status_code": 403,
                "message": "You have reached the maximum number of attempts for this quiz."
            })
            return frappe.response["message"]

        # Prepare quiz details
        quiz_details = {
            "title": quiz_doc.title,
            "course": quiz_doc.course,
            "instruction": quiz_doc.instruction,
            "to_date": quiz_doc.to_date.strftime('%Y-%m-%d %H:%M:%S') if quiz_doc.make_the_quiz_availability else None,
            "duration": quiz_doc.duration if quiz_doc.is_time_bound else None,
            "number_of_attempts": quiz_doc.number_of_attempts,
            "attempts_left": attempts_left,  
            "grading_basis": quiz_doc.grading_basis,
            "total_grades": quiz_doc.total_grades
        }

        # Construct the response
        frappe.response.update({
            "status_code": 200,
            "message": "Quiz details fetched successfully",
            "data": quiz_details
        })
        return frappe.response["message"]

    # Construct the error response
    except Exception as e:
        frappe.response.update({
            "status_code": 500,
            "message": "An error occurred while fetching quiz details."
        })
        return frappe.response["message"]


@frappe.whitelist(allow_guest=True)
def get_quiz(quiz_name="2874210861"):
    try:
        # Fetch the quiz document
        quiz_doc = frappe.get_doc("LMS Quiz", quiz_name)

        # Prepare the quiz details
        quiz = {
            "title": quiz_doc.title,
            "course": quiz_doc.course,
            "duration": quiz_doc.duration if quiz_doc.is_time_bound else None,
            "quiz_question": []
        }

        # Fetch each question linked to the quiz
        for question_row in quiz_doc.quiz_question:
            question_doc = frappe.get_doc("Question", question_row.question_link)
            question_details = {
                "name": question_doc.name,
                "question": question_doc.question,
                "question_type": question_doc.question_type,
                "question_options": [
                    {"option": option.option}
                    for option in question_doc.question_options
                ],
                "question_grade": question_row.question_grade,
            }
            quiz["quiz_question"].append(question_details)

        # Add the total number of questions
        quiz["questions_number"] = len(quiz["quiz_question"])

        # Construct the success response
        frappe.response.update({
            "status_code": 200,
            "message": "Quiz questions fetched successfully",
            "data": quiz
        })
        return frappe.response["message"]

    except Exception as e:
        # General error handling
        frappe.response.update({
            "status_code": 500,
            "message": f"An error occurred while fetching quiz details: {str(e)}"
        })
    return frappe.response["message"]
