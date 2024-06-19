# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


class CourseEnrollmentTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.course_enrollment_course.course_enrollment_course import CourseEnrollmentCourse
		from academia.academia.doctype.course_enrollment_student.course_enrollment_student import CourseEnrollmentStudent
		from frappe.types import DF

		academic_program: DF.Literal["", "All Programs", "Specific Program"]
		academic_term: DF.Link
		academic_year: DF.Link
		courses: DF.Table[CourseEnrollmentCourse]
		faculty: DF.Link
		level: DF.Literal["", "All Levels", "Specific Level"]
		specific_level: DF.Link | None
		specific_program: DF.Link | None
		students: DF.Table[CourseEnrollmentStudent]
	# end: auto-generated types

	child_table_data1 = []

	@frappe.whitelist()
	def get_courses(self):
		global child_table_data1
		child_table_data = []
		child_data = {}

		if not self.academic_year:
			frappe.throw(_("Mandatory field - Academic Year"))
		elif not self.academic_term:
			frappe.throw(_("Mandatory field - Academic Term"))
		elif self.academic_program == "All Programs":
			if self.level == "All Levels":
				#code for get all prpgrams with all levels
				course_study = frappe.get_list('Course Study', fields='*')
				for course in course_study:
					child_table_data.append(course)

			elif self.level == "Specific Level":
				if self.specific_level:
					#code for get all programs with a specific level
					course_study = frappe.get_list('Course Study', fields='*')
					for course in course_study:
						if course['level'] == self.specific_level:
							child_table_data.append(course)
					

				else:
					frappe.throw(_("Mandatory field - Specific Level"))
			else:
				frappe.throw(_("Mandatory field - Level"))

		elif self.academic_program == "Specific Program":
			if self.specific_program:
				if self.level == "All Levels":
					#code for get specific program with all levels
					course_study = frappe.get_list('Course Study', fields='*')
					for course in course_study:
						if course['program'] == self.specific_program:
							child_table_data.append(course)

				elif self.level == "Specific Level":
					if self.specific_level:
						#code for get specific program with specific level
						course_study = frappe.get_list('Course Study', fields='*')
						for course in course_study:
							if course['program'] == self.specific_program:
								if course['level'] == self.specific_level:
									child_table_data.append(course)
						
					else:
						frappe.throw(_("Mandatory field - Specific Level"))
				else:
					frappe.throw(_("Mandatory field - Level"))
			else:
				frappe.throw(_("Mandatory field - Specific Program"))
		else:
			frappe.throw(_("Mandatory field - Academic Program"))

		# child_table_data1 = child_table_data

		if child_table_data:
			return child_table_data
		else:
			frappe.throw(_("No courses Found"))