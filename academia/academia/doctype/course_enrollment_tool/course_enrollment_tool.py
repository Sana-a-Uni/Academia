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

	courses1 = []

	@frappe.whitelist()
	def get_courses(self):
		global courses1
		courses = []
		students = []
		child_data = {}

		if not self.academic_year:
			frappe.throw(_("Mandatory field - Academic Year"))
		elif not self.academic_term:
			frappe.throw(_("Mandatory field - Academic Term"))
		elif self.academic_program == "All Programs":
			if self.level == "All Levels":
				#code for get all prpgrams with all levels
				program_enrollment = frappe.get_list('Program Enrollment', fields='*')
				for student in program_enrollment:
					students.append(student)

				course_study = frappe.get_list('Course Study', fields='*')
				for course in course_study:
					courses.append(course)

			elif self.level == "Specific Level":
				if self.specific_level:
					#code for get all programs with a specific level
					program_enrollment = frappe.get_list('Program Enrollment', fields='*')
					for student in program_enrollment:
						students.append(student)

					course_study = frappe.get_list('Course Study', fields='*')
					for course in course_study:
						if course['level'] == self.specific_level:
							courses.append(course)
					

				else:
					frappe.throw(_("Mandatory field - Specific Level"))
			else:
				frappe.throw(_("Mandatory field - Level"))

		elif self.academic_program == "Specific Program":
			if self.specific_program:
				if self.level == "All Levels":
					#code for get specific program with all levels
					program_enrollment = frappe.get_list('Program Enrollment', fields='*')
					for student in program_enrollment:
						if student['program'] == self.specific_program:
							students.append(student)

					course_study = frappe.get_list('Course Study', fields='*')
					for course in course_study:
						if course['program'] == self.specific_program:
							courses.append(course)

				elif self.level == "Specific Level":
					if self.specific_level:
						#code for get specific program with specific level
						program_enrollment = frappe.get_list('Program Enrollment', fields='*')
						for student in program_enrollment:
							if student['program'] == self.specific_program:
								students.append(student)

						course_study = frappe.get_list('Course Study', fields='*')
						for course in course_study:
							if course['program'] == self.specific_program:
								if course['level'] == self.specific_level:
									courses.append(course)
						
					else:
						frappe.throw(_("Mandatory field - Specific Level"))
				else:
					frappe.throw(_("Mandatory field - Level"))
			else:
				frappe.throw(_("Mandatory field - Specific Program"))
		else:
			frappe.throw(_("Mandatory field - Academic Program"))

		# courses1 = courses

		if not courses and not students:
			frappe.throw(_("No courses and students Found"))
		elif not students:
			return {"courses": courses}
			frappe.throw(_("No students Found"))
		elif not courses:
			return {"students": students}
			frappe.throw(_("No courses Found"))
		else:
			return {
				"students": students,
				"courses": courses
			}

	@frappe.whitelist()
	def generate(self):
		students = []
		for student in self.students:
			student_data = student.as_dict()
			students.append(student_data)
			for course in self.courses:
				course_data = course.as_dict()
				if course_data['program'] == student_data['program']:
					course_enrollment = frappe.new_doc('Course Enrollment')
					course_enrollment.student = student_data['student']
					course_enrollment.student_name = student_data['student_name']
					course_enrollment.academic_program = student_data['program']
					course_enrollment.course = course_data['course_code']
					course_enrollment.student_batch = student_data['student_batch']
					course_enrollment.academic_year = self.academic_year
					course_enrollment.academic_term = self.academic_term
					course_enrollment.save()

		frappe.msgprint('Students Enrolled Succesfully...')
