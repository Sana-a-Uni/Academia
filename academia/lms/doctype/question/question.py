# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Question(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.lms.doctype.question_options.question_options import QuestionOptions
		from frappe.types import DF

		course: DF.Link | None
		faculty_member: DF.Link | None
		question: DF.TextEditor | None
		question_options: DF.Table[QuestionOptions]
		question_type: DF.Literal["", "Multiple Choice", "Multiple Answer"]
	# end: auto-generated types
	pass
