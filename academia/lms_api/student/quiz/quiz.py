import frappe
from datetime import datetime
from typing import Dict, Any, List
import json

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
def get_quiz(quiz_name):
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



@frappe.whitelist(allow_guest=True)
def create_quiz_attempt():
    data = json.loads(frappe.request.data)

    student = data.get('student')
    quiz = data.get('quiz')
    start_time = data.get('start_time')
    answers = data.get('answers')

    if not student or not quiz or not start_time or not answers:
        frappe.throw("Missing required parameters")

    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = datetime.now()

    quiz_doc = frappe.get_doc('LMS Quiz', quiz)

    time_taken = end_time - start_time

    total_grade = 0
    correct_answers = 0
    incorrect_answers = 0
    incomplete_answers = 0

    quiz_answer_list = []
    for answer in answers:
        question = frappe.get_doc('Question', answer.get('question'))
        correct_options = [option.option for option in question.question_options if option.is_correct]
        question_grade = 0

        for quiz_question in quiz_doc.quiz_question:
            if quiz_question.question_link == answer.get('question'):
                question_grade = quiz_question.question_grade
                break

        selected_options = answer.get('selected_option')
        if not selected_options:
            incomplete_answers += 1
            selected_options_str = ""
            is_correct = False
            grade = 0
        elif set(selected_options if isinstance(selected_options, list) else [selected_options]) == set(correct_options):
            correct_answers += 1
            total_grade += question_grade
            selected_options_str = ', '.join(selected_options) if isinstance(selected_options, list) else str(selected_options)
            is_correct = True
            grade = question_grade
        else:
            incorrect_answers += 1
            selected_options_str = ', '.join(selected_options) if isinstance(selected_options, list) else str(selected_options)
            is_correct = False
            grade = 0

        quiz_answer_list.append({
            'question': answer.get('question'),
            'selected_option': selected_options_str,
            'is_correct': is_correct,
            'grade': grade
        })

    # Create new quiz attempt
    quiz_attempt = frappe.get_doc({
        'doctype': 'Quiz Attempt',
        'student': student,
        'quiz': quiz,
        'grade': total_grade,
        'number_of_correct_answers': correct_answers,
        'number_of_incorrect_answers': incorrect_answers,
        'number_of_unanswered_questions': incomplete_answers,
        'start_time': start_time,
        'end_time': end_time,
        'time_taken': time_taken.total_seconds(), 
        'quiz_answer': quiz_answer_list
    })
    quiz_attempt.insert()
    frappe.db.commit()

    # Determine final score based on the number of attempts and grading basis
    if quiz_doc.number_of_attempts == 1:
        final_score = total_grade
        attempts_taken = 1
    else:
        attempts = frappe.get_all('Quiz Attempt', filters={'student': student, 'quiz': quiz}, fields=['grade'])
        attempts.append({'grade': total_grade})  # Include the current attempt

        grading_basis = quiz_doc.grading_basis
        if grading_basis == 'Highest Grade':
            final_score = max(attempt['grade'] for attempt in attempts)
        elif grading_basis == 'Latest Attempt':
            final_score = attempts[-1]['grade']
        elif grading_basis == 'Average of Attempts':
            final_score = sum(attempt['grade'] for attempt in attempts) / len(attempts)

        attempts_taken = len(attempts)

    # Create or update Quiz Result
    existing_result = frappe.get_all('Quiz Result', filters={'student': student, 'quiz': quiz}, fields=['name'])
    if existing_result:
        quiz_result = frappe.get_doc('Quiz Result', existing_result[0]['name'])
        quiz_result.grade = final_score
        quiz_result.attempts_taken = attempts_taken
        quiz_result.save()
    else:
        quiz_result = frappe.get_doc({
            'doctype': 'Quiz Result',
            'student': student,
            'quiz': quiz,
            'grade': final_score,
            'attempts_taken': attempts_taken
        })
        quiz_result.insert()

    frappe.db.commit()

    # Return the name of the current quiz attempt
    frappe.response["status_code"] = 200
    frappe.response["message"] = "Quiz Completed successfully"
    frappe.response["quiz_attempt_id"] = quiz_attempt.name



@frappe.whitelist(allow_guest=True)
def get_quiz_result(quiz_attempt_id="dee2e6f2c0"):
    try:
        quiz_attempt = frappe.get_doc('Quiz Attempt', quiz_attempt_id)
        quiz_doc = frappe.get_doc('LMS Quiz', quiz_attempt.quiz)

        time_taken = quiz_attempt.time_taken
        days, remainder = divmod(time_taken, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_taken_str = ""
        if days > 0:
            time_taken_str += f"{int(days)}d "
        if hours > 0:
            time_taken_str += f"{int(hours)}h "
        if minutes > 0:
            time_taken_str += f"{int(minutes)}m "
        time_taken_str += f"{int(seconds)}s"

        questions_with_grades = []
        for answer in quiz_attempt.quiz_answer:
            question = frappe.get_doc('Question', answer.question)
            question_grade = 0

            for quiz_question in quiz_doc.quiz_question:
                if quiz_question.question_link == answer.question:
                    question_grade = quiz_question.question_grade
                    break

            questions_with_grades.append({
                'question': question.question,
                'grade': question_grade,
                'user_grade': answer.grade
            })

        response_data = {
            'course_name': quiz_attempt.course,
            'quiz': quiz_doc.title,
            'grade': quiz_attempt.grade,
            'number_of_correct_answers': quiz_attempt.number_of_correct_answers,
            'number_of_incorrect_answers': quiz_attempt.number_of_incorrect_answers,
            'number_of_unanswered_questions': quiz_attempt.number_of_unanswered_questions,
            'number_of_questions': len(quiz_doc.quiz_question),
            'start_time': quiz_attempt.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': quiz_attempt.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'time_taken': time_taken_str,
            'grade_out_of': quiz_attempt.grade_out_of,
            'questions_with_grades': questions_with_grades  
        }

        frappe.response["status_code"] = 200
        frappe.response["data"] = response_data

    except Exception as e:
        frappe.response["status_code"] = 500
        frappe.response["message"] = "An error occurred while fetching the quiz result"
        return {'error': str(e)}