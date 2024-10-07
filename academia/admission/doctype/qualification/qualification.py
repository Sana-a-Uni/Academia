# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Qualification(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		college: DF.Data | None
		country: DF.Data | None
		department: DF.Data | None
		estimation: DF.Data | None
		graduation_year: DF.Data | None
		name1: DF.Data | None
		name_series: DF.Literal["ADM-SAP-.YYYY.-"]
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		percentage: DF.Data | None
		qualification: DF.Data | None
		role: DF.Data | None
		specialty: DF.Data | None
		university: DF.Data | None
	# end: auto-generated types
	pass
