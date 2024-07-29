# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CompensatoryLesson(Document):
	def on_submit(self):
		self.create_lesson_record()
	
	def before_cancel(self):
		lesson_list =frappe.db.get_list('Lesson', pluck='name', filters = {"custom_compensatory_lesson_reference": self.name})
		for lesson in lesson_list:
			frappe.delete_doc('Lesson', lesson)
	
	def create_lesson_record(self):
			lesson = frappe.get_doc(
				dict(
					doctype="Lesson",
					lesson_type="Compensatory Lesson",
					schedule_template_version="v1_جدول الفصل الدراسي الاول للعام لبجامعي 1444 (2023-2024 ) كلية الحاسوب",
					schedule_template="جدول الفصل الدراسي الاول للعام الجامعي 1446 (2024-2025 ) كلية الحاسوب",
					is_multi_group=self.is_multi_group,
					academic_year=self.academic_year,
					academic_term=self.academic_term,
					faculty=self.faculty,
					program=self.program,
					level=self.level,
					instructor=self.instructor,
					course_type=self.course_type,
					course=self.course,
					group=self.group,
					subgroup=self.subgroup,
					room=self.room,
					date=self.date,
					from_time=self.from_time,
					to_time=self.to_time,
					table_hfgk=self.multi_group,
					custom_compensatory_lesson_reference = self.name
				)
			)
			lesson.save()

@frappe.whitelist()
def get_multi_groups_data(name):
	is_multi_group = frappe.get_list("Lesson Attendance", fields=["is_multi_group"], filters={"name":name})
	multi_group_table = []
	if is_multi_group:
		multi_group_table = frappe.get_list('Multi Lesson Template',
											parent_doctype = "Lesson Attendance", 
											filters={'parent':name}, 
											fields=["program" , "level", "group"])

	return multi_group_table