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

		academic_program: DF.Literal["", "All Programs", "Specific Program"]
		academic_term: DF.Link
		academic_year: DF.Link
		based_on: DF.Literal["", "Program", "Batch"]
		courses: DF.Table[CourseStudyCourse]
		current_level: DF.ReadOnly
		faculty: DF.Link
		level: DF.Literal["", "All Levels", "Specific Level"]
		program_specification: DF.ReadOnly | None
		specific_level: DF.Link | None
		specific_program: DF.Link | None
		student_batch: DF.Link | None
	# end: auto-generated types
	

	@frappe.whitelist()
	def get_courses(self):
		child_table_data = []
		child_data = {}

		if self.based_on == "Program":
			#by Program
			if not self.student_batch:
				if self.academic_program == "All Programs":
					if self.level == "All Levels":
						#code for get all prpgrams with all levels
						program_specifications = frappe.get_list('Program Specification', fields='*')
						for program in program_specifications:
							program_specification_doc = frappe.get_doc("Program Specification", program.name)
							for child in program_specification_doc.table_ytno:
								child_data = child.as_dict()

								course_exists_in_course_study = frappe.db.exists('Course Study', {'course_name': child_data['course_name']})
								if not course_exists_in_course_study:
									student_batch = frappe.get_list("Student Batch", fields='*')
									for batch in student_batch:
										if batch.program_specification == child_data['parent']:
											child_data['batch'] = batch.name

									child_table_data.append(child_data)
						frappe.msgprint(str(child_table_data))

					elif self.level == "Specific Level":
						if self.specific_level:
							#code for get all programs with a specific level
							program_specifications = frappe.get_list('Program Specification', fields='*')
							for program in program_specifications:
								program_specification_doc = frappe.get_doc("Program Specification", program.name)
								for child in program_specification_doc.table_ytno:
									child_data = child.as_dict()

									course_exists_in_course_study = frappe.db.exists('Course Study', {'course_name': child_data['course_name']})
									if not course_exists_in_course_study:
										student_batch = frappe.get_list("Student Batch", fields='*')
										for batch in student_batch:
											if batch.program_specification == child_data['parent']:
												child_data['batch'] = batch.name

										child_table_data.append(child_data)
							filterd_data_by_specific_level = [d for d in child_table_data if d.get("study_level") == self.specific_level]
							child_table_data  = filterd_data_by_specific_level

						else:
							frappe.throw(_("Mandatory field - Specific Level"))
					else:
						frappe.throw(_("Mandatory field - Level"))

				elif self.academic_program == "Specific Program":
					if self.specific_program:
						if self.level == "All Levels":
							#code for get specific program with all levels
							#frappe.throw(_("Mandatory field -0000000000Specific Level"))
							program_specification_doc = frappe.get_doc("Program Specification", self.specific_program)
							for child in program_specification_doc.table_ytno:
								child_data = child.as_dict()

								course_exists_in_course_study = frappe.db.exists('Course Study', {'course_name': child_data['course_name']})
								if not course_exists_in_course_study:
									student_batch = frappe.get_list("Student Batch", fields='*')
									for batch in student_batch:
										if batch.program_specification == child_data['parent']:
											child_data['batch'] = batch.name

									child_table_data.append(child_data)

						elif self.level == "Specific Level":
							if self.specific_level:
								#code for get specific program with specific level
								program_specification_doc = frappe.get_doc("Program Specification", self.specific_program)
								for child in program_specification_doc.table_ytno:
									child_data = child.as_dict()

									course_exists_in_course_study = frappe.db.exists('Course Study', {'course_name': child_data['course_name']})
									if not course_exists_in_course_study:
										student_batch = frappe.get_list("Student Batch", fields='*')
										for batch in student_batch:
											if batch.program_specification == child_data['parent']:
												child_data['batch'] = batch.name

										child_table_data.append(child_data)

								filterd_data_by_specific_level = [d for d in child_table_data if d.get("study_level") == self.specific_level]
								child_table_data  = filterd_data_by_specific_level

							else:
								frappe.throw(_("Mandatory field - Specific Level"))
						else:
							frappe.throw(_("Mandatory field - Level"))
					else:
						frappe.throw(_("Mandatory field - Specific Program"))
				else:
					frappe.throw(_("Mandatory field - Academic Program"))
			else:
				frappe.throw(_("Mandatory field - Student Batch"))
		elif self.based_on == "Batch":
			#by Batch
			if self.student_batch:
				#code for get by batch
				if self.program_specification == "Finished":
					frappe.throw(_("This Batch is already finished..."))
				else:
					program_specification_doc = frappe.get_doc("Program Specification", self.program_specification)
					for child in program_specification_doc.table_ytno:
						child_data = child.as_dict()
			
						course_exists_in_course_study = frappe.db.exists('Course Study', {'course_name': child_data['course_name']})
						if not course_exists_in_course_study:
							child_data['batch'] = self.student_batch
							child_table_data.append(child_data)

			else:
				frappe.throw(_("Mandatory field - Student Batch"))
		else:
			frappe.throw(_("Mandatory field - Based On"))	
		


		if child_table_data:
			return child_table_data
		else:
			frappe.throw(_("No courses Found"))

	@frappe.whitelist()
	def generate_courses(self):
		if not self.academic_year:
			frappe.throw(_("Mandatory field - Academic Year"))
		elif not self.academic_term:
			frappe.throw(_("Mandatory field - Academic term"))
		else:	

			for cour in self.courses:
				child_hours_data = {}

				key = cour.course_code
				course_specification_doc = frappe.get_doc("Course Specification", key)
				for child in course_specification_doc.credit_hours:

					child_hours = child.as_dict()
					child_hours_data[child.hour_type] = child_hours

				num = len(child_hours_data)
				if num < 1:
					frappe.msgprint(_("You have to add at least one row for the credit hours table in {0} course specification...").format(cour.course_name))
				elif num >=1 :
					for i, hour_table in child_hours_data.items():
						course_exists_in_course_study = frappe.db.exists('Course Study', {'course_code': cour.course_code , 'course_type': hour_table['hour_type']})
						if course_exists_in_course_study:
							frappe.msgprint(_("This course {0} already generated...").format(cour.course_name +' '+ hour_table['hour_type']))
						else:
							course_study = frappe.new_doc("Course Study")
							course_study.course_code = cour.course_code
							course_study.student_batch = cour.batch
							course_study.program = cour.parent
							course_study.academic_year = self.academic_year
							course_study.academic_term = self.academic_term
							course_study.level = cour.study_level
							course_study.course_type = hour_table['hour_type']
							course_study.hours = hour_table['hours']
							course_study.suitable_env = hour_table['suitable_env']
							course_study.save()	

			frappe.msgprint(_("Generated Successfully..."))	
