# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
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
		company: DF.Link | None
		department: DF.Link | None
		designation: DF.Link | None
		email: DF.Data | None
		employee: DF.Link
		employee_name: DF.Data | None
		evaluation_template: DF.Link | None
		evaluation_type: DF.Literal["", "Department Head Evaluate his Faculty Members", "Faculty Members Evaluate their Department Head", "Faculty Members Evaluate Employee"]
		faculty_members: DF.Table[FacultyMemberEvaluationForm]
	# end: auto-generated types
	pass


# FN: Whitelist function to get faculty member
@frappe.whitelist()
def get_faculty_members_from_department(department):
	faculty_members = frappe.db.sql(f"""
		SELECT name
        FROM `tabFaculty Member`
		WHERE department = '{department}'
	""", as_dict=True)
	return faculty_members
# End of the function


@frappe.whitelist()
def get_faculty_members_from_company(company):
	faculty_members = frappe.db.sql(f"""
		SELECT name
        FROM `tabFaculty Member`
		WHERE company = '{company}'
	""", as_dict=True)
	return faculty_members