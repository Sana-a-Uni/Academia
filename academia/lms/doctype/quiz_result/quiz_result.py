# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class QuizResult(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		attempts_taken: DF.Int
		course: DF.Link | None
		grade: DF.Float
		quiz: DF.Link | None
		student: DF.Link | None
	# end: auto-generated types
	pass
