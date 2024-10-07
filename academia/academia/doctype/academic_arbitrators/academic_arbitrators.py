# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AcademicArbitrators(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_rank: DF.Data | None
		arbitrator_name: DF.Link
		country: DF.Data | None
		faculty: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		scientific_degree: DF.Data | None
		university: DF.Link | None
	# end: auto-generated types
	pass
