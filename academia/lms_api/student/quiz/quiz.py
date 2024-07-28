import frappe
from datetime import datetime
from typing import Dict, Any, List
import json
import random


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
def get_quiz_instruction(quiz_name: str) -> Dict[str, Any]:
    try:
        quiz_doc = frappe.get_doc("LMS Quiz", quiz_name)

        # Prepare quiz details
        quiz_details = {
            "title": quiz_doc.title,
            "course": quiz_doc.course,
            "instruction": quiz_doc.instruction,
            "to_date": quiz_doc.to_date.strftime('%Y-%m-%d %H:%M:%S') if quiz_doc.make_the_quiz_availability else None,
            "duration": quiz_doc.duration if quiz_doc.is_time_bound else None,
            "number_of_attempts": quiz_doc.number_of_attempts,
            # "attempts_left": attempts_left,
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

    except Exception as e:
        frappe.response.update({
            "status_code": 500,
            "message": "An error occurred while fetching quiz details."
        })
        return frappe.response["message"]


@frappe.whitelist(allow_guest=True)
def get_quiz(quiz_name: str ="2874210861", student_id: str="EDU-STU-2024-00001"):
    try:
        # Fetch the quiz document
        quiz_doc = frappe.get_doc("LMS Quiz", quiz_name)
        
        # Check the number of attempts left for the student
        quiz_results = frappe.get_all('Quiz Result', filters={'student': student_id, 'quiz': quiz_name}, fields=['attempts_taken'])
        current_attempts = quiz_results[0]['attempts_taken'] if quiz_results else 0

        # Check if the student has reached the maximum number of attempts
        if current_attempts >= quiz_doc.number_of_attempts:
            frappe.response.update({
                "status_code": 403,
                "message": "You have reached the maximum number of attempts for this quiz."
            })
            return frappe.response["message"]

        # Prepare the quiz details
        quiz = {
            "title": quiz_doc.title,
            "course": quiz_doc.course,
            "is_time_bound":quiz_doc.is_time_bound,
            "to_date": quiz_doc.to_date.strftime('%Y-%m-%d %H:%M:%S'),
            "duration": quiz_doc.duration if quiz_doc.is_time_bound else None,
            "quiz_question": []
        }

        # Fetch each question linked to the quiz
        for question_row in quiz_doc.quiz_question:
            question_doc = frappe.get_doc("Question", question_row.question_link)
            question_options = [
                {"option": option.option}
                for option in question_doc.question_options
            ]

            # Randomize the order of options if required
            if quiz_doc.randomize_question_order:
                random.shuffle(question_options)

            question_details = {
                "name": question_doc.name,
                "question": question_doc.question,
                "question_type": question_doc.question_type,
                "question_options": question_options,
                "question_grade": question_row.question_grade,
            }
            quiz["quiz_question"].append(question_details)

        # Randomize the question order if required
        if quiz_doc.randomize_question_order:
            random.shuffle(quiz["quiz_question"])

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
def get_quiz_result(quiz_attempt_id):
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

            question_data = {
                'question': question.question,
            }
            if quiz_doc.show_question_score:
                question_data.update({
                    'grade': question_grade,
                    'user_grade': answer.grade,
                })

            questions_with_grades.append(question_data)

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
            'show_correct_answer': quiz_doc.show_correct_answer,
            'show_question_score': quiz_doc.show_question_score,
            'questions_with_grades': questions_with_grades  
        }

        frappe.response["status_code"] = 200
        frappe.response["data"] = response_data

    except Exception as e:
        frappe.response["status_code"] = 500
        frappe.response["message"] = "An error occurred while fetching the quiz result"
        return {'error': str(e)}

@frappe.whitelist(allow_guest=True)
def get_all_quiz_attempts(course_name: str = "00", student_id: str = "EDU-STU-2024-00001") -> Dict[str, Any]:
    try:
        # Get all quiz attempts for the specified student in the specified course
        quiz_attempts = frappe.get_all(
            'Quiz Attempt',
            filters={
                'course': course_name,
                'student': student_id
            },
            fields=['name', 'quiz', 'grade', 'grade_out_of', 'start_time', 'end_time', 'time_taken']
        )

        # Convert and format values for response
        result = []
        for attempt in quiz_attempts:
            time_taken = attempt['time_taken']
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

            # Get the quiz title and show_correct_answer from LMS Quiz
            quiz_doc = frappe.get_doc('LMS Quiz', attempt['quiz'])
            quiz_title = quiz_doc.title
            show_correct_answer = quiz_doc.show_correct_answer

            # Update formatted values in the attempts list
            attempt_data = {
                "name": attempt['name'],
                'quiz': quiz_title,
                'grade': attempt['grade'],
                'grade_out_of': attempt['grade_out_of'],
                'start_time': attempt['start_time'].strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': attempt['end_time'].strftime('%Y-%m-%d %H:%M:%S'),
                'time_taken': time_taken_str,
                'show_correct_answer': show_correct_answer
            }
            result.append(attempt_data)

        # Prepare the response
        frappe.response.update({
            "status_code": 200,
            "message": "Quiz attempts fetched successfully",
            "data": result
        })
        
        return frappe.response["message"]
    
    except Exception as e:
        # Prepare the error response in case of an issue
        frappe.response.update({
            "status_code": 500,
            "message": f"An error occurred while fetching the quiz attempts: {str(e)}"
        })
        
    return frappe.response["message"]


@frappe.whitelist(allow_guest=True)
def get_quiz_attempt_details(quiz_attempt_id="6e8dbb9b7b"):
    try:
        quiz_attempt = frappe.get_doc('Quiz Attempt', quiz_attempt_id)
        quiz_doc = frappe.get_doc('LMS Quiz', quiz_attempt.quiz)

        # Check if the correct answers should be shown
        if not quiz_doc.show_correct_answer:
            frappe.response["status_code"] = 403
            frappe.response["message"] = "Access to correct answers is restricted."
            return frappe.response

        questions_with_answers = []
        for answer in quiz_attempt.quiz_answer:
            question = frappe.get_doc('Question', answer.question)
            question_options = [{"option": option.option, "is_correct": option.is_correct} for option in question.question_options]
            
            questions_with_answers.append({
                'question': question.question,
                'question_type': question.question_type,  
                'selected_option': answer.selected_option,
                'is_correct': answer.is_correct,
                'correct_option': ', '.join([opt['option'] for opt in question_options if opt['is_correct']]),
                'question_options': question_options
            })

        frappe.response["status_code"] = 200
        frappe.response["questions_with_answers"] = questions_with_answers

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Quiz Attempt Details Error")
        frappe.response["status_code"] = 500
        frappe.response["message"] = f"An error occurred while fetching the quiz attempt details: {str(e)}"
        frappe.response["error"] = str(e)

    return frappe.response
