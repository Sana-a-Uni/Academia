# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LessonTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.multi_lesson_template.multi_lesson_template import MultiLessonTemplate
		from frappe.types import DF

		academic_term: DF.Link
		academic_year: DF.Link
		course: DF.Link
		course_type: DF.Literal["", "Theoretical", "Practical"]
		faculty: DF.Link
		from_time: DF.Time
		group: DF.Link | None
		instructor: DF.Link
		is_multi_group: DF.Check
		lesson_type: DF.Literal["", "Ordinary Lesson", "Compensatory Lesson"]
		level: DF.Link
		monday: DF.Check
		program: DF.Link
		room: DF.Link
		saturday: DF.Check
		schedule_template: DF.ReadOnly | None
		schedule_template_version: DF.Link
		sub_group: DF.Data | None
		sunday: DF.Check
		table_ocar: DF.Table[MultiLessonTemplate]
		thursday: DF.Check
		to_time: DF.Time
		tuesday: DF.Check
		wednesday: DF.Check
	# end: auto-generated types
	pass
