# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AssignmentAssessment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.lms.doctype.assignment_assessment_details.assignment_assessment_details import AssignmentAssessmentDetails
		from frappe.types import DF

		amended_from: DF.Link | None
		assessment_date: DF.Datetime | None
		assignment: DF.Link | None
		assignment_assessment_details: DF.Table[AssignmentAssessmentDetails]
		assignment_submission: DF.Link | None
		faculty_member: DF.Link | None
		feedback: DF.TextEditor | None
		grade: DF.Float
		student: DF.Link | None
	# end: auto-generated types
	pass
