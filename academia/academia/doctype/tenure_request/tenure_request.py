# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _



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
		date: DF.Date | None
		department: DF.Link | None
		evaluations: DF.TableMultiSelect[Evaluations]
		faculty: DF.Link | None
		faculty_member: DF.Link
		faculty_member_name: DF.Data | None
		naming_series: DF.Literal["TENUREQ-.YYYY.-.faculty_member_name.-"]
	# end: auto-generated types
	pass

	def before_submit(self):
		faculty_member = frappe.get_doc("Faculty Member", self.faculty_member)
		if not faculty_member.is_eligible_for_granting_tenure:
			frappe.throw(_("Dear {0}, you are not eligible for granting tenure.").format(self.faculty_member_name))


@frappe.whitelist()
def get_evaluations(faculty_member):
	evaluations = frappe.db.sql(f"""
		SELECT name
        FROM `tabAcademic Evaluation`
		WHERE evaluatee_party = '{faculty_member}' AND docstatus = 1
	""", as_dict=True)
	return evaluations