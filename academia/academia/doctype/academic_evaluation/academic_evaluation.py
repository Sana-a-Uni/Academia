# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AcademicEvaluation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.evaluation_detail.evaluation_detail import EvaluationDetail
		from frappe.types import DF

		academic_rank: DF.Link | None
		academic_term: DF.Link
		academic_year: DF.Link
		amended_from: DF.Link | None
		attachment: DF.Attach | None
		company: DF.Link | None
		date: DF.Date | None
		department: DF.Link | None
		designation: DF.Link | None
		email: DF.Data
		evaluatee_party: DF.DynamicLink
		evaluatee_party_name: DF.Data | None
		evaluatee_party_type: DF.Literal
		evaluation_details: DF.Table[EvaluationDetail]
		evaluator_party: DF.DynamicLink
		evaluator_party_name: DF.Data | None
		evaluator_party_type: DF.Literal
		faculty: DF.Link | None
		naming_series: DF.Literal["Unknown-", "EVAL-EMP-FM-.department.-.evaluatee_party_name.-.YYYY.-", "EVAL-FM-EMP-.department.-.evaluatee_party_name.-.YYYY.-", "EVAL-FM-STD-.department.-.evaluatee_party_name.-.YYYY.-"]
		notes: DF.SmallText | None
		template: DF.Link | None
	# end: auto-generated types
	

# FN: Whitelist function to get academic_evaluation criteria
@frappe.whitelist()
def get_evaluation_criteria(template):
	templates = frappe.db.sql(f"""
		SELECT ec.criterion
        FROM `tabEvaluation Criteria` ec 
        JOIN `tabEvaluation Criteria Template` ect
        ON ec.parent = ect.name
		WHERE ect.name = '{template}'
	""", as_dict=True)
	return templates
# End of the function



@frappe.whitelist()
def get_department_head(department):
    department_head = frappe.db.get_value('Employee', {'department': department, 'designation': 'Department Head'}, 'name')
    return department_head
