# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class CompensatoryLesson(Document):
	def validate(self):
		self.validate_duplicate_reqested()
		if self.workflow_state == "Approval Pending By Department Head":
			self.validate_mandatory()
						  
	def on_submit(self):
		self.create_lesson_record()
	
	def before_cancel(self):
		lesson_list =frappe.db.get_list('Lesson', pluck='name', filters = {"custom_compensatory_lesson_reference": self.name})
		for lesson in lesson_list:
			frappe.delete_doc('Lesson', lesson)
	
	def validate_duplicate_reqested(self):
		if self.workflow_state == "Draft":
			compensator_lesson_list =frappe.db.get_list('Compensatory Lesson', fields=['name', 'workflow_state'],filters = {"lesson_attendance": self.lesson_attendance})
			if compensator_lesson_list:
				for lesson in compensator_lesson_list:
					if lesson["workflow_state"] in ["Approval Pending By Academic Manager","Approval Pending By Department Head","Approval Pending By Dean of the College","Approved"]:
						frappe.throw(_("You already have reqested Compensatory Lesson <a href='/app/compensatory-lesson/{}'>{}</a> for this Lesson Attendance and his status is {}")
						  .format(lesson["name"],lesson["name"],lesson["workflow_state"]))

	def validate_mandatory(self):
		"""Validates all mandatory fields"""
		fields = [
			"date",
			"room",
			"from_time",
			"to_time",
		]  

		for d in fields:
			if not self.get(d):
				frappe.throw(_("{0} is mandatory").format(self.meta.get_label(d)))
	
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
	def show_lecture_info(self):
		data = []
		row = {}
		total_absent = 0
		total_present = 0
		total_compensatory_lesson = 0
		filters = {"docstatus": 1}

		for field, value in {"faculty":self.faculty ,"academic_year":self.academic_year ,"academic_term":self.academic_term ,
						"program":self.program ,"level":self.level ,"faculty_member":self.instructor ,"course_type":self.course_type ,"course":self.course ,
						"group":self.group,"subgroup":self.subgroup,"multi_group":self.multi_group}.items():
				if value:
					filters[field] = value
		
		row["total_absent"] = self.get_total(filters, "status", "Absent"),
		row["total_present"] = self.get_total(filters, "status", "Present")
		filters.pop("faculty_member")
		filters["instructor"] = self.instructor
		row["total_compensatory_lesson"] = frappe.db.count("Compensatory Lesson", filters)
		data.append(row)

		return data


	def get_total(self,filters, field, value):
		count = 0
		filters[field] = value
		
		count =frappe.db.count("Lesson Attendance", filters)
		filters.pop(field)
		
		return count
	

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
