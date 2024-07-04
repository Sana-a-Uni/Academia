# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate

class FacultyMemberSettings(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_rank: DF.Link | None
		date_of_joining: DF.Date | None
		is_eligible_for_granting_tenure: DF.Check
		naming_series: DF.Literal["ACAD-FM-S-.YYYY.-.MM.-.####."]
		probation_period_end_date: DF.Date | None
		valid_from: DF.Date | None
		valid_upto: DF.Date | None
	# end: auto-generated types
	pass

	def validate(self):
		self.validate_dates()

	def validate_dates(self):
		if self.valid_from and self.valid_upto:
			if getdate(self.valid_from) > getdate(self.valid_upto):
				frappe.throw(_("Valid From Date must be lesser than Valid Upto Date."))