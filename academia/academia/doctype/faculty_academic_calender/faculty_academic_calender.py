# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FacultyAcademicCalender(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.academic_calender__procedure.academic_calender__procedure import (
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
	pass
