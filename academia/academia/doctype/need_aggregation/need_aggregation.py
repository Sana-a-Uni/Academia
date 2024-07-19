# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class NeedAggregation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.approved_department_need.approved_department_need import ApprovedDepartmentNeed
		from frappe.types import DF

		amended_from: DF.Link | None
		approved_department_needs: DF.Table[ApprovedDepartmentNeed]
		general_application_terms: DF.Text | None
	# end: auto-generated types
	pass
