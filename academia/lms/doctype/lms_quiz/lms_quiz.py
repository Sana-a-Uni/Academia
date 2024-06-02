# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LMSQuiz(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.lms.doctype.quiz_question.quiz_question import QuizQuestion
		from frappe.types import DF

		course: DF.Link | None
		duration: DF.Duration | None
		faculty_member: DF.Link | None
		from_date: DF.Datetime | None
		grading_basis: DF.Literal["Highest Grade", "Latest Attempt", "Average of Attempts"]
		instruction: DF.SmallText | None
		is_time_bound: DF.Check
		make_the_quiz_availability: DF.Check
		max_attempts: DF.Int
		multiple_attempts: DF.Check
		quiz_question: DF.Table[QuizQuestion]
		student_group: DF.Link | None
		title: DF.Data
		to_date: DF.Datetime | None
		total_grades: DF.Float
	# end: auto-generated types
	pass
