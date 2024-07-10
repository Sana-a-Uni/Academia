import frappe
import json

@frappe.whitelist()
def create_quiz():
    data = json.loads(frappe.request.data)
    try:
        questions = create_questions(data.get("quiz_question"))
        create_quiz_doc(data, questions)

    except Exception as e:
        frappe.response["status_code"] = 500
        frappe.response["message"] = "An error occurred while creating the quiz."
        return

    frappe.response["status_code"] = 200
    frappe.response["message"] = "Quiz created successfully"

def create_quiz_doc(data, questions):
    quiz_doc = frappe.new_doc("LMS Quiz")
    quiz_doc.course = data.get("course")
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

def create_question(question_data):
    question_doc = frappe.new_doc("Question")
    question_doc.update(question_data)
   
    question_doc.save()
    return question_doc

def create_questions(questions_data):
    questions = []
    for question_data in questions_data:
        question_doc = create_question(question_data)
        questions.append(question_doc)
    return questions


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