# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate



class ProbationPeriods(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_rank: DF.Link
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		probation_period: DF.Data
		valid_from: DF.Date
		valid_upto: DF.Date | None
	# end: auto-generated types
	pass

	def validate(self):
		self.validate_dates()
		self.get_date_of_joining()

	def validate_dates(self):
		if self.valid_from and self.valid_upto:
			if getdate(self.valid_from) > getdate(self.valid_upto):
				frappe.throw(_("Valid From Date must be lesser than Valid Upto Date."))
				

	# def get_date_of_joining(self):
	# 	if self.faculty_member:
	# 		faculty_member = frappe.get_doc("Faculty Member", self.faculty_member)
	# 		self.date_of_joining = faculty_member.date_of_joining_in_university