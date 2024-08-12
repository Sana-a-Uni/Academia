# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import (
	add_days,
	cint,
	cstr,
	format_date,
	get_datetime,
	get_link_to_form,
	getdate,
	nowdate,
)

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
		attendance_date: DF.Date
		course: DF.Link
		course_type: DF.Literal["", "Theoretical", "Practical"]
		early_exit: DF.Check
		early_exit_note: DF.SmallText | None
		early_exit_time: DF.Time | None
		faculty: DF.Link
		faculty_member: DF.Link
		faculty_member_name: DF.ReadOnly | None
		from_time: DF.Time
		group: DF.Link | None
		is_multi_group: DF.Check
		late_entry: DF.Check
		late_entry_note: DF.SmallText | None
		late_entry_time: DF.Time | None
		lesson: DF.Link | None
		lesson_type: DF.Literal["", "Ordinary Lesson", "Compensatory Lesson"]
		level: DF.Link | None
		multi_groups: DF.Table[MultiLessonTemplate]
		program: DF.Link | None
		room: DF.Link
		schedule_template: DF.Link
		schedule_template_version: DF.Link
		status: DF.Literal["", "Present", "Absent"]
		subgroup: DF.Data | None
		teaching_hours: DF.Float
		to_time: DF.Time
	# end: auto-generated types
	
	def validate(self):
		if (getdate(self.attendance_date) > getdate(nowdate())):
			frappe.throw(
				_("Attendance can not be marked for future dates: {0}").format(
					frappe.bold(format_date(self.attendance_date)),
				)
			)
	
	def on_submit(self):
		self.send_absence_notification()
	
	def send_absence_notification(self):
		if self.status == "Absent":
			instructor = frappe.get_doc("Faculty Member", self.faculty_member)
			user_id = instructor.email
			
			if user_id:
				subject = "Absence Notification"
				message = f"{instructor.faculty_member_name},\n\nYou have been marked as absent for {self.attendance_date}.\n\nPlease request a make-up lecture as soon as possible."
				
				# Send system notification
				notification = frappe.new_doc("Notification Log")
				notification.update({
					"for_user": user_id,
					"subject": subject,
					"email_content": message,
					"document_type": self.doctype,
					"document_name": self.name,
				})
				notification.insert(ignore_permissions=True)
				frappe.db.commit()