# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TenureEvaluationRequest(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.tenure_evaluation_criteria.tenure_evaluation_criteria import TenureEvaluationCriteria
		from frappe.types import DF

		academic_rank: DF.Link
		academic_term: DF.Link | None
		academic_year: DF.Link | None
		amended_from: DF.Link | None
		attachment: DF.Attach | None
		company: DF.Link
		department: DF.Link
		template: DF.Link | None
		tenure_evaluation_criteria: DF.Table[TenureEvaluationCriteria]
	# end: auto-generated types
	

# FN: Whitelist function to get evaluation criteria
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


