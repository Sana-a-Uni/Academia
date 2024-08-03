# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class HourRateList(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		currency: DF.Link
		date_of_apply: DF.Date | None
		default: DF.Check
		enabled: DF.Check
		hour_rate_list_name: DF.Data
	# end: auto-generated types
	pass
