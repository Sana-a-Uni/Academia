# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LessonAttendance(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.multi_lesson_template.multi_lesson_template import MultiLessonTemplate
		from frappe.types import DF

		academic_term: DF.Link
		academic_year: DF.Link
		amended_from: DF.Link | None
		attendance_date: DF.Date | None
		course: DF.Link | None
		course_type: DF.Literal["", "Theoretical", "Practical"]
		early_exit: DF.Check
		early_exit_note: DF.SmallText | None
		early_exit_time: DF.Time | None
		faculty: DF.Link
		faculty_member: DF.Link | None
		faculty_member_name: DF.ReadOnly | None
		from_time: DF.Time | None
		group: DF.Link | None
		is_multi_group: DF.Check
		late_entry: DF.Check
		late_entry_note: DF.SmallText | None
		late_entry_time: DF.Time | None
		lesson: DF.Link | None
		lesson_type: DF.Literal["", "Ordinary Lesson", "Compensatory Lesson"]
		level: DF.Link | None
		multi_groups: DF.Table[MultiLessonTemplate]
		program: DF.Link
		room: DF.Link | None
		schedule_template: DF.Link | None
		schedule_template_version: DF.Link | None
		status: DF.Literal["", "Present", "Absent"]
		subgroup: DF.Data | None
		to_time: DF.Time | None
	# end: auto-generated types
	pass
