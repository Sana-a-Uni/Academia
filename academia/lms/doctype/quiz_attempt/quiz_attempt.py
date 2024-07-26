# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class QuizAttempt(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.lms.doctype.quiz_answer.quiz_answer import QuizAnswer
		from frappe.types import DF

		course: DF.Link | None
		end_time: DF.Datetime | None
		grade: DF.Float
		grade_out_of: DF.Float
		number_of_correct_answers: DF.Int
		number_of_incorrect_answers: DF.Int
		number_of_unanswered_questions: DF.Int
		quiz: DF.Link | None
		quiz_answer: DF.Table[QuizAnswer]
		start_time: DF.Datetime | None
		student: DF.Link | None
		time_taken: DF.Duration | None
	# end: auto-generated types
	pass
