# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LMSAssignment(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.lms.doctype.assessment_criteria.assessment_criteria import AssessmentCriteria
		from academia.lms.doctype.attachment_files.attachment_files import AttachmentFiles
		from frappe.types import DF

		assessment_criteria: DF.Table[AssessmentCriteria]
		assignment_title: DF.Data
		attachment_file: DF.Table[AttachmentFiles]
		course: DF.Link | None
		faculty_member: DF.Link | None
		from_date: DF.Datetime | None
		instruction: DF.SmallText | None
		make_the_assignment_availability: DF.Check
		question: DF.TextEditor | None
		student_group: DF.Link | None
		to_date: DF.Datetime | None
		total_grades: DF.Float
	# end: auto-generated types
	pass
