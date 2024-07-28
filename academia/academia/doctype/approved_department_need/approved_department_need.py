# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ApprovedDepartmentNeed(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_specialty: DF.Link | None
		academic_year: DF.Link
		application_requirements: DF.SmallText | None
		faculty: DF.Link
		faculty_department: DF.Link
		name: DF.Int | None
		number_of_positions: DF.Data
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		reference_to_department_need_approval: DF.Link | None
		scientific_degree: DF.Link
		specialist_field: DF.Data | None
	# end: auto-generated types
	pass
