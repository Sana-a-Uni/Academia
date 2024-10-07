# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class CompensatoryLesson(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.multi_lesson_template.multi_lesson_template import MultiLessonTemplate
		from academia.academic_attendance.doctype.proposed_times.proposed_times import ProposedTimes
		from frappe.types import DF

		academic_term: DF.Link
		academic_year: DF.Link
		amended_from: DF.Link | None
		cancelled_reason: DF.Data | None
		course: DF.Link
		course_type: DF.Literal["", "Theoretical", "Practical"]
		date: DF.Date | None
		faculty: DF.Link
		faculty_department: DF.Link | None
		from_time: DF.Time | None
		group: DF.Link | None
		instructor: DF.Link
		instructor_name: DF.Data | None
		is_multi_group: DF.Check
		is_transfer: DF.Literal["", "1", "2"]
		lesson_attendance: DF.Link
		level: DF.Link | None
		multi_groups: DF.Table[MultiLessonTemplate]
		program: DF.Link | None
		proposed_times: DF.Table[ProposedTimes]
		reason: DF.Data
		reason_for_rejection: DF.Data | None
		room: DF.Link | None
		subgroup: DF.Data | None
		to_time: DF.Time | None
		workflow_state: DF.Link | None
	# end: auto-generated types
	def validate(self):
		self.validate_duplicate_reqested()
		if self.workflow_state == "Approval Pending By Department Head":
			self.validate_mandatory()
						  
	def on_submit(self):
		self.create_lesson_record()
	
	def before_cancel(self):
		lesson_list =frappe.db.get_list('Lesson', pluck='name', filters = {"compensatory_lesson_reference": self.name})
		for lesson in lesson_list:
			frappe.delete_doc('Lesson', lesson)
			frappe.msgprint(_("The Lesson that Linked to this request was Deleted"))
	
	def validate_duplicate_reqested(self):
		if self.workflow_state == "Draft":
			compensator_lesson_list =frappe.db.get_list('Compensatory Lesson', fields=['name', 'workflow_state'],filters = {"lesson_attendance": self.lesson_attendance})
			if compensator_lesson_list:
				for lesson in compensator_lesson_list:
					if lesson["workflow_state"] in ["Approval Pending By Academic Manager","Approval Pending By Department Head","Approval Pending By Faculty Dean","Approved"]:
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
			try:
				version = frappe.get_last_doc('Schedule Template Version',filters={"faculty":self.faculty, "academic_year":self.academic_year, "academic_term":self.academic_term,"is_active":1})
			except:
				frappe.throw(_("There was not active Schedule Template Version,please contact to Academic Manager first to active current version that you are use for schedule"))
			lesson = frappe.get_doc(
				dict(
					doctype="Lesson",
					lesson_type="Compensatory Lesson",
					schedule_template_version=version.name,
					schedule_template=version.schedule_template,
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
					table_hfgk=self.multi_groups,
					compensatory_lesson_reference = self.name
				)
			)
			lesson.save()
			frappe.msgprint(_("Lesson create for this request"))
	
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
						"group":self.group,"subgroup":self.subgroup}.items():
				if value:
					filters[field] = value

		if self.is_multi_group:
			records = []
			multi_groups = frappe.get_list('Multi Lesson Template',
											parent_doctype = "Compensatory Lesson",
											filters={'parent':self.name},
											fields=["program" , "level", "group"])
			records = self.get_some_records(multi_groups, filters,"Lesson Attendance")
				
			for record in records:
				status = frappe.db.get_value("Lesson Attendance", record, 'status')
				if status == "Present":
					total_present += 1
				if status == "Absent":
					total_absent += 1

			row["total_present"] = total_present
			row["total_absent"] = total_absent

			filters["instructor"] = self.instructor
			total_compensatory_lesson = len(self.get_some_records(multi_groups, filters,"Compensatory Lesson"))		
			row["total_compensatory_lesson"] = total_compensatory_lesson
		else :
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
	

	def get_some_records(self, multi_groups, filters, doctype):
		parent_list = []
		multi_group_parent = []
		valid_values = []

		for group in multi_groups:
				filters["program"] = group.program
				filters["level"] = group.level
				filters["group"] = group.group
				if doctype == "Lesson Attendance":
					names = self.get_multi_group_parent(filters)
				if doctype == "Compensatory Lesson":
					names = self.get_multi_group_compensatory_lesson(filters)
				for name in names:
					parent_list.append(name.name)

		parent_list = list(dict.fromkeys(parent_list))

		for parent in parent_list:
			num = 0
			multi_group_parent = frappe.get_list('Multi Lesson Template',
										parent_doctype = doctype, 
										filters={'parent':parent}, 
										fields=["program" , "level", "group"])
			for value in multi_group_parent:
				if value in multi_groups:
					num += 1
			if num == len(multi_group_parent):
				valid_values.append(parent)
		
		return valid_values


	def get_multi_group_parent(self,filters):
		conditions = ""
		if filters.get("faculty"):
			conditions += "AND attendance.faculty = %(faculty)s"
		if filters.get("academic_year"):
			conditions += "AND attendance.academic_year = %(academic_year)s"
		if filters.get("academic_term"):
			conditions += "AND attendance.academic_term = %(academic_term)s"
		if filters.get("faculty_member"):
			conditions += "AND attendance.faculty_member = %(faculty_member)s"
		if filters.get("course_type"):
			conditions += "AND attendance.course_type = %(course_type)s"
		if filters.get("course"):
			conditions += "AND attendance.course = %(course)s"
		if filters.get("program"):
			conditions += "AND multi_group.program = %(program)s"
		if filters.get("level"):
			conditions += "AND multi_group.level = %(level)s"
		if filters.get("group"):
			conditions += "AND multi_group.group = %(group)s"
		
		query = f"""
			SELECT
				attendance.name as name
			FROM
				`tabLesson Attendance` as attendance
			JOIN
				`tabMulti Lesson Template` as multi_group
			ON
				attendance.name = multi_group.parent 
			WHERE
				1=1 AND multi_group.parenttype = 'Lesson Attendance' 
				AND attendance.docstatus = 1
				{conditions}
		"""

		return frappe.db.sql(query, filters, as_dict=True)
	
	def get_multi_group_compensatory_lesson(self,filters):		
		query = f"""
			SELECT
				attendance.name as name
			FROM
				`tabCompensatory Lesson` as attendance
			JOIN
				`tabMulti Lesson Template` as multi_group
			ON
				attendance.name = multi_group.parent 
			WHERE
				1=1 AND multi_group.parenttype = 'Compensatory Lesson' 
				AND attendance.faculty = %(faculty)s
				AND attendance.academic_year = %(academic_year)s
				AND attendance.academic_term = %(academic_term)s
				AND attendance.instructor = %(instructor)s
				AND attendance.course_type = %(course_type)s
				AND attendance.course = %(course)s
				AND multi_group.program = %(program)s
				AND multi_group.level = %(level)s
				AND multi_group.group = %(group)s
				AND attendance.docstatus = 1
		"""

		return frappe.db.sql(query, filters, as_dict=True)

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