# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AcademicEntitlementDetails(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_hour_rate: DF.Data | None
		academic_rank: DF.Link | None
		course: DF.Link | None
		course_type: DF.Literal["", "Theoretical", "Practical"]
		faculty_member: DF.Link | None
		faculty_member_name: DF.Data | None
		group: DF.Link | None
		lesson_type: DF.Literal["", "Ordinary Lesson", "Compensatory Lesson"]
		level: DF.Link | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		program: DF.Link | None
		status: DF.Literal["Unoccupied", "occupied"]
		subgroup: DF.Data | None
		total: DF.Data | None
		total_hours: DF.Int
		total_lectures: DF.Int
	# end: auto-generated types
	pass
