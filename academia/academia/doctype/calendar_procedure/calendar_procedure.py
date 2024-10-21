# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class CalendarProcedure(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		procedure_code: DF.Data
		procedure_name: DF.Data
		procedure_name_english: DF.Data | None
	# end: auto-generated types
	pass
