# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EvaluationFormGeneratorTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.faculty_member_evaluation_form.faculty_member_evaluation_form import FacultyMemberEvaluationForm
		from frappe.types import DF

		academic_term: DF.Link
		academic_year: DF.Link
		department: DF.Link | None
		employee: DF.Link
		employee_name: DF.Data | None
		evaluation_template: DF.Link | None
		faculty_members: DF.Table[FacultyMemberEvaluationForm]
	# end: auto-generated types
	pass
