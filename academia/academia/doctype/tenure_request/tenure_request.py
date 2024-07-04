# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class TenureRequest(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.faculty_member_evaluation.faculty_member_evaluation import FacultyMemberEvaluation
		from frappe.types import DF

		academic_rank: DF.Link
		amended_from: DF.Link | None
		company: DF.Link
		department: DF.Link | None
		evaluations: DF.TableMultiSelect[FacultyMemberEvaluation]
		faculty: DF.Link | None
		faculty_member: DF.Link
		faculty_member_name: DF.Data | None
		naming_series: DF.Literal["TENUREQ-.YYYY.-.faculty_member_name.-"]
	# end: auto-generated types
	pass
