# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AcademicCalenderProcedure(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		end_date: DF.Date | None
		note: DF.Text | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		procedure: DF.Data
		procedure_type: DF.Literal["", "period", "one day"]
		start_date: DF.Date
	# end: auto-generated types
	pass
