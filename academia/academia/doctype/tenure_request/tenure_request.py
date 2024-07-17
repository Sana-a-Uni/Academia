# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TenureRequest(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.evaluations.evaluations import Evaluations
		from frappe.types import DF

		academic_rank: DF.Link
		amended_from: DF.Link | None
		company: DF.Link
		department: DF.Link | None
		evaluations: DF.TableMultiSelect[Evaluations]
		faculty: DF.Link | None
		faculty_member: DF.Link
		faculty_member_name: DF.Data | None
		naming_series: DF.Literal["TENUREQ-.YYYY.-.faculty_member_name.-"]
	# end: auto-generated types
	pass


@frappe.whitelist()
def get_evaluations(faculty_member):
	evaluations = frappe.db.sql(f"""
		SELECT name
        FROM `tabAcademic Evaluation`
		WHERE evaluatee_party = '{faculty_member}' AND docstatus = 1
	""", as_dict=True)
	return evaluations