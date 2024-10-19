# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


class FacultyAcademicCalender(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.academic_calendar_procedure.academic_calendar_procedure import (
			AcademicCalenderProcedure,
		)
		from frappe.types import DF

		academic_calendar_term_one: DF.Table[AcademicCalenderProcedure]
		academic_calendar_term_three: DF.Table[AcademicCalenderProcedure]
		academic_calendar_term_two: DF.Table[AcademicCalenderProcedure]
		academic_calendar_type: DF.Literal["", "Bachelor Studies", "Post Graduate Studies"]
		academic_system_type: DF.Literal["", "Semester System", "Credit Hours System", "Annual System"]
		academic_year: DF.Link
		faculty: DF.Link
		university_calendar: DF.Link | None
	# end: auto-generated types

	# start get university calendar term one
	@frappe.whitelist()
	def get_university_calendar_term_one(self):
		if self.university_calendar:
			if not self.faculty:
				frappe.throw(_("Mandatory field - Faculty"))
			elif not self.academic_calendar_type:
				frappe.throw(_("Mandatory field - Academic Calendar Type"))
			elif not self.academic_year:
				frappe.throw(_("Mandatory field - Academic Year"))
			elif not self.academic_system_type:
				frappe.throw(_("Mandatory field - Academic System Type"))
			else:
				academic_calendar_term_one = []
				university_calendar = frappe.get_doc("University Academic Calendar", self.university_calendar)
				for term_one in university_calendar.academic_calendar_term_one:
					term_one_row_data = term_one.as_dict()
					academic_calendar_term_one.append(term_one_row_data)

		else:
			frappe.throw(_("Mandatory field - University Calendar"))

		if not academic_calendar_term_one:
			frappe.throw(_("No academic_calendar_term_one Found"))
		else:
			return academic_calendar_term_one

	# end get university calendar term one

	# start get university calendar term two
	@frappe.whitelist()
	def get_university_calendar_term_two(self):
		if self.university_calendar:
			if not self.faculty:
				frappe.throw(_("Mandatory field - Faculty"))
			elif not self.academic_calendar_type:
				frappe.throw(_("Mandatory field - Academic Calendar Type"))
			elif not self.academic_year:
				frappe.throw(_("Mandatory field - Academic Year"))
			elif not self.academic_system_type:
				frappe.throw(_("Mandatory field - Academic System Type"))
			else:
				academic_calendar_term_two = []
				university_calendar = frappe.get_doc("University Academic Calendar", self.university_calendar)
				for term_two in university_calendar.academic_calendar_term_two:
					term_two_row_data = term_two.as_dict()
					academic_calendar_term_two.append(term_two_row_data)

		else:
			frappe.throw(_("Mandatory field - University Calendar"))

		if not academic_calendar_term_two:
			frappe.throw(_("No academic_calendar_term_two Found"))
		else:
			return academic_calendar_term_two

	# end get university calendar term two

	# start get university calendar term three
	@frappe.whitelist()
	def get_university_calendar_term_three(self):
		if self.university_calendar:
			if not self.faculty:
				frappe.throw(_("Mandatory field - Faculty"))
			elif not self.academic_calendar_type:
				frappe.throw(_("Mandatory field - Academic Calendar Type"))
			elif not self.academic_year:
				frappe.throw(_("Mandatory field - Academic Year"))
			elif not self.academic_system_type:
				frappe.throw(_("Mandatory field - Academic System Type"))
			else:
				academic_calendar_term_three = []
				university_calendar = frappe.get_doc("University Academic Calendar", self.university_calendar)
				for term_three in university_calendar.academic_calendar_term_three:
					term_three_row_data = term_three.as_dict()
					academic_calendar_term_three.append(term_three_row_data)

		else:
			frappe.throw(_("Mandatory field - University Calendar"))

		if not academic_calendar_term_three:
			frappe.throw(_("No academic_calendar_term_three Found"))
		else:
			return academic_calendar_term_three

	# end get university calendar term three
