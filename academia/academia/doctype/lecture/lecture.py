# Copyright (c) 2023, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Lecture(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_program: DF.Link | None
		academic_term: DF.Data | None
		academic_week: DF.Data | None
		academic_year: DF.Link | None
		color: DF.Color | None
		course: DF.Link | None
		date: DF.Date | None
		description: DF.TextEditor | None
		duration: DF.Duration | None
		faculty: DF.Link | None
		faculty_department: DF.Link | None
		faculty_member: DF.Link | None
		from_time: DF.Time | None
		lecture_type: DF.Literal["", "Theoretical", "Practical"]
		published: DF.Check
		room: DF.Link | None
		status: DF.Literal["", "Completed", "Scheduled", "Overdue", "Unscheduled"]
		student_group: DF.Link | None
		to_time: DF.Time | None
		video: DF.Attach | None
	# end: auto-generated types
	pass
