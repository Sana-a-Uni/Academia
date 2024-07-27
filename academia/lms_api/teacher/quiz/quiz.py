import json
import frappe
from datetime import datetime
from typing import List, Dict, Any

def validate_general_data(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate general data fields for the quiz.

    :param data: The input data for the quiz
    :return: A dictionary containing error messages for invalid fields
    """
    errors: Dict[str, str] = {}

    if not data.get("title"):
        errors["title"] = "Title is required."
    
    if data.get("is_time_bound") == 1 and not data.get("duration"):
        errors["duration"] = "Duration is required when quiz is time bound."
    
    if data.get("multiple_attempts") == 1 and not data.get("grading_basis"):
        errors["grading_basis"] = "Grading basis is required when multiple attempts are allowed."
    
    return errors

def validate_date_fields(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Validate date fields for the quiz availability.

    :param data: The input data for the quiz
    :return: A dictionary containing error messages for invalid date fields
    """
    errors: Dict[str, str] = {}

    if data.get("make_the_quiz_availability") == 1:
        from_date = data.get("from_date")
        to_date = data.get("to_date")
        if not from_date:
            errors["from_date"] = "From date is required when quiz availability is set."
        if not to_date:
            errors["to_date"] = "To date is required when quiz availability is set."
        if from_date and to_date:
            validate_dates_order_and_future(from_date, to_date, errors)
    
    return errors

def validate_dates_order_and_future(from_date: str, to_date: str, errors: Dict[str, str]) -> None:
    """
    Validate the from_date and to_date fields.

    :param from_date: The start date of the quiz availability
    :param to_date: The end date of the quiz availability
    :param errors: The dictionary to add error messages to
    """
    from_date_dt = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S')
    to_date_dt = datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S')
    if from_date_dt >= to_date_dt:
        errors["from_date"] = "From date must be earlier than To date."
    if from_date_dt <= datetime.now():
        errors["from_date"] = "From date must be in the future."

def validate_quiz_questions(questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Validate the list of questions for the quiz.

    :param questions: The list of questions to validate
    :return: A list of error messages for invalid questions
    """
    errors: List[Dict[str, Any]] = []
    seen_questions = set()

    if not questions or len(questions) == 0:
        errors.append({"question": "At least one question is required."})

    for i, question in enumerate(questions):
        question_errors: Dict[str, str] = {}
        question_text = question.get("question")
        question_type = question.get("question_type")
        question_options = tuple(sorted((opt.get("option"), opt.get("is_correct")) for opt in question.get("question_options", [])))
        question_signature = (question_text, question_type, question_options)

        if question_signature in seen_questions:
            question_errors["question"] = f"Duplicate question found at index {i}. Each question must be unique."
        else:
            seen_questions.add(question_signature)

        if not validate_question_grade(question, question_errors):
            question_errors["question_grade"] = "Question grade must be a positive number."

        if not question.get('name'):
            validate_question_fields(question, question_errors, i)

        if question_errors:
            errors.append({"index": i, "errors": question_errors})

    return errors

def validate_question_grade(question: Dict[str, Any], question_errors: Dict[str, str]) -> bool:
    """
    Validate the grade of a question.

    :param question: The question data
    :param question_errors: The dictionary to add error messages to
    :return: True if the grade is valid, False otherwise
    """
    if question.get("question_grade") is None or question.get("question_grade") == "":
        question_errors["question_grade"] = "Question grade is required."
        return False
    elif question.get("question_grade") < 0:
        question_errors["question_grade"] = "Question grade must be a positive number."
        return False
    return True

def validate_question_fields(question: Dict[str, Any], question_errors: Dict[str, str], i: int) -> None:
    """
    Validate the required fields of a question.

    :param question: The question data
    :param question_errors: The dictionary to add error messages to
    :param i: The index of the question in the list
    """
    if not question.get("question_type"):
        question_errors["question_type"] = "Question type is required."
    if not question.get("question"):
        question_errors["question"] = "Question text is required."
    question_errors.update(validate_question_options(question, i))

def validate_question_options(question: Dict[str, Any], question_index: int) -> Dict[str, str]:
    """
    Validate the options of a question.

    :param question: The question data
    :param question_index: The index of the question in the list
    :return: A dictionary containing error messages for invalid options
    """
    errors: Dict[str, str] = {}
    options = question.get("question_options", [])

    if question.get("question_type") in ["Multiple Choice", "Multiple Answer"]:
        if len(options) < 2:
            errors["question_options"] = f"At least two options are required for question {question_index + 1}."
        correct_options = [opt for opt in options if opt.get("is_correct")]
        if question.get("question_type") == "Multiple Choice" and len(correct_options) != 1:
            errors["question_options"] = f"Exactly one correct option is required for Multiple Choice question {question_index + 1}."
        if question.get("question_type") == "Multiple Answer" and len(correct_options) < 1:
            errors["question_options"] = f"At least one correct option is required for Multiple Answer question {question_index + 1}."

    check_duplicate_question_options(options, errors, question_index)
    return errors

def check_duplicate_question_options(options: List[Dict[str, Any]], errors: Dict[str, str], question_index: int) -> None:
    """
    Check for duplicate options in a question.

    :param options: The list of options
    :param errors: The dictionary to add error messages to
    :param question_index: The index of the question in the list
    """
    seen_options = set()
    for opt in options:
        option_text = opt.get("option", "").strip().lower()
        if option_text in seen_options:
            errors["question_options"] = f"Duplicate option '{opt.get('option')}' found in question {question_index + 1}."
            break
        seen_options.add(option_text)

def prepare_questions_for_creation(data: Dict[str, Any]) -> None:
    """
    Prepare questions by adding necessary fields before creation.

    :param data: The input data for the quiz
    """
    for question in data.get("quiz_questions"):
        if 'name' not in question:
            question["course"] = data.get("course")
            question["faculty_member"] = data.get("faculty_member")

def create_quiz_document(data: Dict[str, Any], questions: List[frappe.Document]) -> None:
    """
    Create the quiz document with associated questions.

    :param data: The input data for the quiz
    :param questions: The list of created question documents
    """
    quiz_doc = frappe.new_doc("LMS Quiz")
    quiz_doc.course = data.get("course")
    quiz_doc.faculty_member = data.get("faculty_member")
    quiz_doc.title = data.get("title")
    quiz_doc.instruction = data.get("instruction")
    quiz_doc.make_the_quiz_availability = data.get("make_the_quiz_availability")

    if data.get("make_the_quiz_availability") == 1:
        quiz_doc.from_date = data.get("from_date")
        quiz_doc.to_date = data.get("to_date")

    quiz_doc.is_time_bound = data.get("is_time_bound")
    if data.get("is_time_bound") == 1:
        quiz_doc.duration = data.get("duration")

    quiz_doc.multiple_attempts = data.get("multiple_attempts")
    if data.get("multiple_attempts") == 1:
        quiz_doc.number_of_attempts = data.get("number_of_attempts")
        quiz_doc.grading_basis = data.get("grading_basis")
    else:
        quiz_doc.number_of_attempts = 1

    quiz_doc.randomize_question_order = data.get("randomize_question_order")
    quiz_doc.show_question_score = data.get("show_question_score")
    quiz_doc.show_correct_answer = data.get("show_correct_answer")

    total_grades = 0
    for question_doc in questions:
        question_row = quiz_doc.append("quiz_question", {})
        question_row.question_link = question_doc.name
        question_row.question_grade = question_doc.get("question_grade")
        total_grades += question_doc.get("question_grade")

    quiz_doc.total_grades = total_grades
    quiz_doc.insert()

def create_question_document(question_data: Dict[str, Any]) -> frappe.Document:
    """
    Create or update a question document.

    :param question_data: The data for the question
    :return: The created or updated question document
    """
    if 'name' in question_data:
        try:
            question_doc = frappe.get_doc("Question", question_data['name'])
            question_doc.question_grade = question_data['question_grade']
        except frappe.DoesNotExistError:
            raise frappe.ValidationError(f"Question {question_data['name']} not found")
    else:
        question_doc = frappe.new_doc("Question")
        question_doc.update(question_data)
        question_doc.course = question_data.get("course")
        question_doc.faculty_member = question_data.get("faculty_member")

    question_doc.save()
    return question_doc

def create_quiz_questions(questions_data: List[Dict[str, Any]]) -> List[frappe.Document]:
    """
    Create question documents for the quiz.

    :param questions_data: The list of question data
    :return: The list of created question documents
    """
    questions: List[frappe.Document] = []
    for question_data in questions_data:
        question_doc = create_question_document(question_data)
        questions.append(question_doc)
    return questions

def handle_validation_error(e: frappe.ValidationError) -> None:
    """
    Handle validation errors during quiz creation.

    :param e: The validation error
    """
    frappe.response["status_code"] = 400
    frappe.response["errors"] = {"general": str(e)}

def handle_general_error(e: Exception) -> None:
    """
    Handle general errors during quiz creation.

    :param e: The general error
    """
    frappe.response["status_code"] = 500
    frappe.response["message"] = "An error occurred while creating the quiz."
    frappe.log_error(frappe.get_traceback(), "Quiz Creation Error")

@frappe.whitelist()
def create_quiz() -> None:
    data = json.loads(frappe.request.data)

    # Perform validation
    errors: Dict[str, Any] = {}
    errors.update(validate_general_data(data))
    errors.update(validate_date_fields(data))
    question_errors = validate_quiz_questions(data.get("quiz_questions", []))

    if question_errors:
        errors["questions"] = question_errors

    if errors:
        frappe.response["status_code"] = 400
        frappe.response["errors"] = errors
        return

    try:
        prepare_questions_for_creation(data)
        questions = create_quiz_questions(data.get("quiz_questions"))
        create_quiz_document(data, questions)
    except frappe.ValidationError as e:
        handle_validation_error(e)
        return
    except Exception as e:
        handle_general_error(e)
        return

    frappe.response["status_code"] = 200
    frappe.response["message"] = "Quiz created successfully"


@frappe.whitelist()
def get_grading_basis_options():
    try:
        # Fetch grading basis options from the 'grading_basis' field in 'LMS Quiz' Doctype
        grading_basis_options = frappe.get_meta('LMS Quiz').get_field('grading_basis').options
        if grading_basis_options:
            # Split options into a list and strip any extra whitespace
            grading_basis_options = [option.strip() for option in grading_basis_options.split('\n')]
        else:
            grading_basis_options = []

        # Update response with options and success status
        frappe.response.update({
            "status_code": 200,
            "data": grading_basis_options
        })
    except Exception as e:
        # On error, update response with error and failure status
        frappe.response.update({
            "status_code": 500,
            "data": [],
            "error": str(e)
        })

@frappe.whitelist()
def get_question_types():
    try:
        question_types = frappe.get_meta('Question').get_field('question_type').options
        if question_types:
            question_types = [option.strip() for option in question_types.split('\n') if option.strip()]
        else:
            question_types = []
            
        # Update response with options and success status
        frappe.response.update({
            "status_code": 200,
            "data": question_types
        })

    except Exception as e:
        # On error, update response with error and failure status
        frappe.response.update({
            "status_code": 500,
            "data": [],
            "error": str(e)
        })



@frappe.whitelist(allow_guest=True)
def get_questions_by_course_and_faculty_member(course_name: str = "00", faculty_member: str = "ACAD-FM-00001") -> Dict[str, Any]:
    try:
        # Fetch questions for the given course and faculty_member
      
        questions: List[Dict[str, Any]] = frappe.get_all(
            "Question",
            fields=['name', 'question', 'question_type'],
            filters={
                'course': course_name,
                'faculty_member': faculty_member,
            },
        )

        questions_data = []

        for question in questions:
            question_doc = frappe.get_doc("Question", question['name'])
            question_details = {
                "name": question_doc.name,
                "question": question_doc.question,
                "question_type": question_doc.question_type,
                "question_options": [
                    {"option": option.option, "is_correct": option.is_correct}
                    for option in question_doc.question_options
                ]
            }
            questions_data.append(question_details)

        # Construct the response
        frappe.response.update({
            "status_code": 200,
            "message": "Questions fetched successfully",
            "data": questions_data
        })
        
        return frappe.response["message"]
    
    # Construct the error response
    except Exception as e:
        frappe.response.update({
            "status_code": 500,
            "message": f"An error occurred while fetching questions: {str(e)}"
        })
        
    return frappe.response["message"]



@frappe.whitelist(allow_guest=True)
def get_quizzes_by_course_and_faculty(course: str="00", faculty_member: str= "ACAD-FM-00001"):
    try:
        # Fetch all quizzes that match the given course and faculty member
        quizzes = frappe.get_all('LMS Quiz',
            filters={
                'course': course,
                'faculty_member': faculty_member
            },
            fields=['name', 'title', 'from_date', 'to_date', 'duration', 'number_of_attempts',  'total_grades']
        )

        # Check if quizzes were found
        if not quizzes:
            frappe.response.update({
                "status_code": 404,
                "message": "No quizzes found for the given course and faculty member."
            })
            return frappe.response["message"]

        # Construct the success response
        frappe.response.update({
            "status_code": 200,
            "message": "Quizzes fetched successfully",
            "data": quizzes
        })
        return frappe.response["message"]

    except Exception as e:
        # General error handling
        frappe.response.update({
            "status_code": 500,
            "message": f"An error occurred while fetching quizzes: {str(e)}"
        })
        return frappe.response["message"]

