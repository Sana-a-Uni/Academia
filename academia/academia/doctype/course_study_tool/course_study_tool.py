# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint
from frappe.model.document import Document


class CourseStudyTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.course_study_course.course_study_course import CourseStudyCourse
		from frappe.types import DF

		academic_program: DF.Literal["", "All Program", "Specific Program"]
		academic_term: DF.Link
		academic_year: DF.Link
		courses: DF.Table[CourseStudyCourse]
		current_level: DF.ReadOnly
		level: DF.Literal["", "All Level", "Specific Level"]
		program_specification: DF.ReadOnly | None
		specific_level: DF.Link | None
		specific_program: DF.Link | None
		student_batch: DF.Link
	# end: auto-generated types
	
	child_table_data1 = []

	def course_exists_in_course_study(course_name):
		return frappe.db.exists('Course Study', {'course_name': course_name})

	@frappe.whitelist()
	def get_courses(self):
		global child_table_data1

		if not self.student_batch:
			frappe.throw(_("Mandatory field - Student Batch"))

		if self.program_specification == "Finished":
			frappe.throw(_("This Batch is already finished..."))
		else:
			program_specification_doc = frappe.get_doc("Program Specification", self.program_specification)
			child_table_data = []

		child_data = {}

		for child in program_specification_doc.table_ytno:
			child_data = child.as_dict()
			
			course_exists_in_course_study = frappe.db.exists('Course Study', {'course_name': child_data['course_name']})
			if not course_exists_in_course_study:
				child_table_data.append(child_data)

		child_table_data1 = child_table_data

		if child_table_data:
			return child_table_data
		else:
			frappe.throw(_("No courses Found"))

	@frappe.whitelist()
	def generate_courses(self):
		for i, cour in enumerate(child_table_data1):
			child_hours_data = {}
		
			key = cour.course + '-'
			course_specification_doc = frappe.get_doc("Course Specification", key)
			for child in course_specification_doc.credit_hours:
				
				child_hours = child.as_dict()
				child_hours_data[child.hour_type] = child_hours

			num = len(child_hours_data)
			if num < 2:
				course_exists_in_course_study = frappe.db.exists('Course Study', {'course_name': cour.course_name})
				if course_exists_in_course_study:
					frappe.msgprint(_("This course {0} already generated...").format(cour.course_name))
				else:
					course_study = frappe.new_doc("Course Study")
					course_study.course_code = cour.course
					course_study.course_name = cour.course_name
					course_study.course_type = cour.course_type
					course_study.save()	
			elif num >=2 :
				for i, hour_table in child_hours_data.items():
					key = cour.course_name +' '+ hour_table['hour_type']
					course_exists_in_course_study = frappe.db.exists('Course Study', {'course_name': key})
					if course_exists_in_course_study:
						frappe.msgprint(_("This course {0} already generated...").format(cour.course_name +' '+ hour_table['hour_type']))
					else:
						course_study = frappe.new_doc("Course Study")
						course_study.course_code = cour.course +' ' + hour_table['hour_type']
						course_study.course_name = cour.course_name + ' '+ hour_table['hour_type']
						course_study.course_type = cour.course_type
						course_study.save()	

		frappe.msgprint(_("Generated Successfully..."))	

