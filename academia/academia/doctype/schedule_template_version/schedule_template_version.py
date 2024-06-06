# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ScheduleTemplateVersion(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_term: DF.ReadOnly | None
		academic_year: DF.ReadOnly | None
		end_date: DF.Date | None
		faculty: DF.ReadOnly | None
		is_active: DF.Check
		schedule_template: DF.Link
		start_date: DF.Date | None
	# end: auto-generated types
	pass
