# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FacultyMemberSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_rank: DF.Link | None
		date_of_joining: DF.Date | None
		effective_date: DF.Date | None
		probation_period: DF.Literal
	# end: auto-generated types
	pass
