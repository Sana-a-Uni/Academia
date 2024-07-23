# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint


class StudentGroupTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from academia.academia.doctype.student_group_student.student_group_student import StudentGroupStudent
		from frappe.types import DF

		based_on: DF.Literal["", "By Sex", "All"]
		capacity: DF.Int
		faculty: DF.Link
		grouping_by: DF.Literal["Theoretical", "Practical", "Theoretical and Practical"]
		practical_capacity: DF.Int
		program: DF.Link
		student_batch: DF.Link
		student_group: DF.Link
		students: DF.Table[StudentGroupStudent]
	# end: auto-generated types

	def rename_field_label(self, field_name, new_label):
		doctype = frappe.get_doc('DocType', 'Student Group')
		for field in doctype.fields:
			if field.fieldname == field_name:
				field.label = new_label
				break
		doctype.save()
	
	@frappe.whitelist()
	def get_students(self):
		students = []

		if self.grouping_by == 'Practical':
			if not self.student_group:
				frappe.throw(_("Mandatory field - Student Group"))
			elif not self.program:
				frappe.throw(_("Mandatory field - Program"))
			elif not self.student_batch:
				frappe.throw(_("Mandatory field - Student Batch"))
			else:
				student_group = frappe.get_doc('Student Group', self.student_group)
				for student in student_group.students:
					student_data = student.as_dict()
					students.append(student_data)
		else:
			if not self.program:
				frappe.throw(_("Mandatory field - Program"))
			elif not self.student_batch:
				frappe.throw(_("Mandatory field - Student Batch"))
			else:
				program_enrollment = frappe.get_list('Program Enrollment', fields='*')
				for student in program_enrollment:
					if student['program'] == self.program and student['student_batch'] == self.student_batch:
						students.append(student)
		
		if not students:
			frappe.throw(_("No students Found"))
		else:
			return students

	@frappe.whitelist()
	def generate_groups_ultra(self):
		students = []
		for student in self.students:
			student_data = student.as_dict()
			students.append(student_data)

		keys = ['student_name', 'gender', 'program']
		cleaned_students = [{k: v for k, v in d.items() if k in keys} for d in students]

		if len(cleaned_students) > 0:
			if self.grouping_by == 'Theoretical':
				if not self.capacity:
					frappe.throw(_("Mandatory field - Capacity"))
				else:
					if self.based_on == 'All':
						# Theoretical All grouping here:
						if len(cleaned_students) % self.capacity == 0:
							groups_size = len(cleaned_students) / self.capacity
							for i in range(int(groups_size)):
								student_group = frappe.new_doc('Student Group')
								student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1)
								student_group.batch = self.student_batch
								student_group.program = self.program
								student_group.group_based_on = self.based_on
								for i in range(self.capacity):
									student_entry = student_group.append('students', {})
									student_entry.update(cleaned_students[0])
									del cleaned_students[0]
								student_group.save()
							frappe.msgprint('Groups Successfully Generated...')
						else:
							groups_size = len(cleaned_students) / self.capacity + 1
							capacity = len(cleaned_students) / int(groups_size)
							for i in range(int(groups_size)):
								if i < len(cleaned_students) % int(groups_size):
									student_group = frappe.new_doc('Student Group')
									student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1)
									student_group.batch = self.student_batch
									student_group.program = self.program
									student_group.group_based_on = self.based_on
									for i in range(int(capacity) + 1):
										student_entry = student_group.append('students', {})
										student_entry.update(cleaned_students[0])
										del cleaned_students[0]
									student_group.save()
								else:
									student_group = frappe.new_doc('Student Group')
									student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1)
									student_group.batch = self.student_batch
									student_group.program = self.program
									student_group.group_based_on = self.based_on
									for i in range(int(capacity)):
										student_entry = student_group.append('students', {})
										student_entry.update(cleaned_students[0])
										del cleaned_students[0]
									student_group.save()
							frappe.msgprint('Groups Successfully Generated...')
					elif self.based_on == 'By Sex':
						males = []
						females = []

						for student in cleaned_students:
							if student['gender'] == 'Male':
								males.append(student)
							elif student['gender'] == 'Female':
								females.append(student)

						if not males:
							self.based_on = 'All'
							frappe.msgprint('There are no Male students found, please set the Based On field to All.')
						elif not females:
							self.based_on = 'All'
							frappe.msgprint('There are no Female students found, please set the Based On field to All.')
						else:
							# Theoretical By Sex grouping here:
							# Males:
							if len(males) % self.capacity == 0:
								groups_size = len(males) / self.capacity
								for i in range(int(groups_size)):
									student_group = frappe.new_doc('Student Group')
									student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1) + ' Males'
									student_group.batch = self.student_batch
									student_group.program = self.program
									student_group.group_based_on = self.based_on
									for i in range(self.capacity):
										student_entry = student_group.append('students', {})
										student_entry.update(males[0])
										del males[0]
									student_group.save()
								frappe.msgprint('Groups Successfully Generated...')
							else:
								groups_size = len(males) / self.capacity + 1
								capacity = len(males) / int(groups_size)
								for i in range(int(groups_size)):
									if i < len(males) % int(groups_size):
										student_group = frappe.new_doc('Student Group')
										student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1) + ' Males'
										student_group.batch = self.student_batch
										student_group.program = self.program
										student_group.group_based_on = self.based_on
										for i in range(int(capacity) + 1):
											student_entry = student_group.append('students', {})
											student_entry.update(males[0])
											del males[0]
										student_group.save()
									else:
										student_group = frappe.new_doc('Student Group')
										student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1) + ' Males'
										student_group.batch = self.student_batch
										student_group.program = self.program
										student_group.group_based_on = self.based_on
										for i in range(int(capacity)):
											student_entry = student_group.append('students', {})
											student_entry.update(males[0])
											del males[0]
										student_group.save()
								frappe.msgprint('Groups Successfully Generated...')
							# Females:
							if len(females) % self.capacity == 0:
								groups_size = len(females) / self.capacity
								for i in range(int(groups_size)):
									student_group = frappe.new_doc('Student Group')
									student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1) + ' Females'
									student_group.batch = self.student_batch
									student_group.program = self.program
									student_group.group_based_on = self.based_on
									for i in range(self.capacity):
										student_entry = student_group.append('students', {})
										student_entry.update(females[0])
										del females[0]
									student_group.save()
								frappe.msgprint('Groups Successfully Generated...')
							else:
								groups_size = len(females) / self.capacity + 1
								capacity = len(females) / int(groups_size)
								for i in range(int(groups_size)):
									if i < len(females) % int(groups_size):
										student_group = frappe.new_doc('Student Group')
										student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1) + ' Females'
										student_group.batch = self.student_batch
										student_group.program = self.program
										student_group.group_based_on = self.based_on
										for i in range(int(capacity) + 1):
											student_entry = student_group.append('students', {})
											student_entry.update(females[0])
											del females[0]
										student_group.save()
									else:
										student_group = frappe.new_doc('Student Group')
										student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1) + ' Females'
										student_group.batch = self.student_batch
										student_group.program = self.program
										student_group.group_based_on = self.based_on
										for i in range(int(capacity)):
											student_entry = student_group.append('students', {})
											student_entry.update(females[0])
											del females[0]
										student_group.save()
								frappe.msgprint('Groups Successfully Generated...')
			elif self.grouping_by == 'Practical':
				if not self.capacity:
					frappe.throw(_("Mandatory field - Capacity"))
				else:
					if len(cleaned_students) % self.capacity == 0:
						groups_size = len(cleaned_students) / self.capacity
						if int(groups_size) > 3:
							frappe.throw(_("Can't generate more then three Practical groups, please add more capacity to continue."))
						else:
							for i in range(int(groups_size)):
								student_group = frappe.get_doc('Student Group', self.student_group)
								table_name = 'students' + str(i+1)
								for i in range(self.capacity): 
									student_entry = student_group.append(table_name, {})
									student_entry.update(cleaned_students[0])
									del cleaned_students[0]
								student_group.save()
							frappe.msgprint('Practical Groups Successfully Generated...')
					else:
						groups_size = len(cleaned_students) / self.capacity + 1
						capacity = len(cleaned_students) / int(groups_size)
						if int(groups_size) > 3:
							frappe.throw(_("Can't generate more then three Practical groups, please add more capacity to continue."))
						else:
							for i in range(int(groups_size)):
								if i < len(cleaned_students) % int(groups_size):
									student_group = frappe.get_doc('Student Group', self.student_group)
									table_name = 'students' + str(i+1)
									for i in range(int(capacity) + 1):
										student_entry = student_group.append(table_name, {})
										student_entry.update(cleaned_students[0])
										del cleaned_students[0]
									student_group.save()
								else:
									student_group = frappe.get_doc('Student Group', self.student_group)
									table_name = 'students' + str(i+1)
									for i in range(int(capacity)):
										student_entry = student_group.append(table_name, {})
										student_entry.update(cleaned_students[0])
										del cleaned_students[0]
									student_group.save()
							frappe.msgprint('Practical Groups Successfully Generated...')
			elif self.grouping_by == 'Theoretical and Practical':
				if not self.capacity:
					frappe.throw(_("Mandatory field - Capacity"))
				elif not self.practical_capacity:
					frappe.throw(_("Mandatory field - Practical Capacity"))
				else:
					if self.based_on == 'All':
						# Theoretical and Practical All grouping here:
						if len(cleaned_students) % self.capacity == 0:
							groups_size = len(cleaned_students) / self.capacity
							for i in range(int(groups_size)):
								student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1)
								student_group = frappe.new_doc('Student Group')
								student_group.student_group_name = student_group_name
								student_group.batch = self.student_batch
								student_group.program = self.program
								student_group.group_based_on = self.based_on
								practical_students = []
								for i in range(self.capacity):
									student_entry = student_group.append('students', {})
									student_entry.update(cleaned_students[0])
									practical_students.append(cleaned_students[0])
									del cleaned_students[0]
								student_group.save()
								# Practical:
								practical_student_group = frappe.get_doc('Student Group', student_group_name)
								if len(practical_students) % self.practical_capacity == 0: 
									practical_groups_size = len(practical_students) / self.practical_capacity
									if int(practical_groups_size) > 3:
										frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
									else:
										for i in range(int(practical_groups_size)):
											table_name = 'students' + str(i+1)
											for i in range(self.practical_capacity):
												student_entry = practical_student_group.append(table_name, {})
												student_entry.update(practical_students[0])
												del practical_students[0]
											practical_student_group.save()
								else:
									practical_groups_size = len(practical_students) / self.practical_capacity +1
									practical_capacity = len(practical_students) / int(practical_groups_size)
									if int(practical_groups_size) > 3:
										frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
									else:
										for j in range(int(practical_groups_size)):
											table_name = 'students' + str(j+1)
											if i < len(practical_students) % int(practical_groups_size):
												for i in range(int(practical_capacity) + 1):
													student_entry = practical_student_group.append(table_name, {})
													student_entry.update(practical_students[0])
													del practical_students[0]
												practical_student_group.save()
											else:
												for i in range(int(practical_capacity)):
													student_entry = practical_student_group.append(table_name, {})
													student_entry.update(practical_students[0])
													del practical_students[0]
												practical_student_group.save()
							frappe.msgprint('Groups Successfully Generated...')
						else:
							groups_size = len(cleaned_students) / self.capacity + 1
							capacity = len(cleaned_students) / int(groups_size)
							for l in range(int(groups_size)):
								if l < len(cleaned_students) % int(groups_size):
									student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(l+1)
									student_group = frappe.new_doc('Student Group')
									student_group.student_group_name = student_group_name
									student_group.batch = self.student_batch
									student_group.program = self.program
									student_group.group_based_on = self.based_on
									practical_students = []
									for i in range(int(capacity) + 1):
										student_entry = student_group.append('students', {})
										student_entry.update(cleaned_students[0])
										practical_students.append(cleaned_students[0])
										del cleaned_students[0]
									student_group.save()
									# Practical:
									practical_student_group = frappe.get_doc('Student Group', student_group_name)
									if len(practical_students) % self.practical_capacity == 0: 
										practical_groups_size = len(practical_students) / self.practical_capacity
										if int(practical_groups_size) > 3:
											frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
										else:
											for i in range(int(practical_groups_size)):
												table_name = 'students' + str(i+1)
												for i in range(self.practical_capacity):
													student_entry = practical_student_group.append(table_name, {})
													student_entry.update(practical_students[0])
													del practical_students[0]
												practical_student_group.save()
									else:
										practical_groups_size = len(practical_students) / self.practical_capacity +1
										practical_capacity = len(practical_students) / int(practical_groups_size)
										if int(practical_groups_size) > 3:
											frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
										else:
											for j in range(int(practical_groups_size)):
												table_name = 'students' + str(j+1)
												if i < len(practical_students) % int(practical_groups_size):
													for i in range(int(practical_capacity) + 1):
														student_entry = practical_student_group.append(table_name, {})
														student_entry.update(practical_students[0])
														del practical_students[0]
													practical_student_group.save()
												else:
													for i in range(int(practical_capacity)):
														student_entry = practical_student_group.append(table_name, {})
														student_entry.update(practical_students[0])
														del practical_students[0]
													practical_student_group.save()
								else:
									student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(l+1)
									student_group = frappe.new_doc('Student Group')
									student_group.student_group_name = student_group_name
									student_group.batch = self.student_batch
									student_group.program = self.program
									student_group.group_based_on = self.based_on
									practical_students = []
									for i in range(int(capacity)):
										student_entry = student_group.append('students', {})
										student_entry.update(cleaned_students[0])
										practical_students.append(cleaned_students[0])
										del cleaned_students[0]
									student_group.save()
									# Practical:
									practical_student_group = frappe.get_doc('Student Group', student_group_name)
									if len(practical_students) % self.practical_capacity == 0: 
										practical_groups_size = len(practical_students) / self.practical_capacity
										if int(practical_groups_size) > 3:
											frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
										else:
											for i in range(int(practical_groups_size)):
												table_name = 'students' + str(i+1)
												for i in range(self.practical_capacity):
													student_entry = practical_student_group.append(table_name, {})
													student_entry.update(practical_students[0])
													del practical_students[0]
												practical_student_group.save()
									else:
										practical_groups_size = len(practical_students) / self.practical_capacity +1
										practical_capacity = len(practical_students) / int(practical_groups_size)
										if int(practical_groups_size) > 3:
											frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
										else:
											for j in range(int(practical_groups_size)):
												table_name = 'students' + str(j+1)
												if i < len(practical_students) % int(practical_groups_size):
													for i in range(int(practical_capacity) + 1):
														student_entry = practical_student_group.append(table_name, {})
														student_entry.update(practical_students[0])
														del practical_students[0]
													practical_student_group.save()
												else:
													for i in range(int(practical_capacity)):
														student_entry = practical_student_group.append(table_name, {})
														student_entry.update(practical_students[0])
														del practical_students[0]
													practical_student_group.save()
							frappe.msgprint('Groups Successfully Generated...')
					elif self.based_on == 'By Sex':
						males = []
						females = []
	
						for student in cleaned_students:
							if student['gender'] == 'Male':
								males.append(student)
							elif student['gender'] == 'Female':
								females.append(student)
	
						if not males:
							self.based_on = 'All'
							frappe.msgprint('There are no Male students found, please set the Based On field to All.')
						elif not females:
							self.based_on = 'All'
							frappe.msgprint('There are no Female students found, please set the Based On field to All.')
						else:
							# Theoretical and Practical By Sex grouping here:
							# Males:
							if len(males) % self.capacity == 0:
								groups_size = len(males) / self.capacity
								for i in range(int(groups_size)):
									student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1) + ' Males'
									student_group = frappe.new_doc('Student Group')
									student_group.student_group_name = student_group_name
									student_group.batch = self.student_batch
									student_group.program = self.program
									student_group.group_based_on = self.based_on
									practical_students = []
									for i in range(self.capacity):
										student_entry = student_group.append('students', {})
										student_entry.update(males[0])
										practical_students.append(males[0])
										del males[0]
									student_group.save()
									# Practical:
									practical_student_group = frappe.get_doc('Student Group', student_group_name)
									if len(practical_students) % self.practical_capacity == 0: 
										practical_groups_size = len(practical_students) / self.practical_capacity
										if int(practical_groups_size) > 3:
											frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
										else:
											for i in range(int(practical_groups_size)):
												table_name = 'students' + str(i+1)
												for i in range(self.practical_capacity):
													student_entry = practical_student_group.append(table_name, {})
													student_entry.update(practical_students[0])
													del practical_students[0]
												practical_student_group.save()
									else:
										practical_groups_size = len(practical_students) / self.practical_capacity +1
										practical_capacity = len(practical_students) / int(practical_groups_size)
										if int(practical_groups_size) > 3:
											frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
										else:
											for j in range(int(practical_groups_size)):
												table_name = 'students' + str(j+1)
												if i < len(practical_students) % int(practical_groups_size):
													for i in range(int(practical_capacity) + 1):
														student_entry = practical_student_group.append(table_name, {})
														student_entry.update(practical_students[0])
														del practical_students[0]
													practical_student_group.save()
												else:
													for i in range(int(practical_capacity)):
														student_entry = practical_student_group.append(table_name, {})
														student_entry.update(practical_students[0])
														del practical_students[0]
													practical_student_group.save()
								frappe.msgprint('Groups Successfully Generated...')
							else:
								groups_size = len(males) / self.capacity + 1
								capacity = len(males) / int(groups_size)
								for l in range(int(groups_size)):
									if l < len(males) % int(groups_size):
										student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(l+1) + ' Males'
										student_group = frappe.new_doc('Student Group')
										student_group.student_group_name = student_group_name
										student_group.batch = self.student_batch
										student_group.program = self.program
										student_group.group_based_on = self.based_on
										practical_students = []
										for i in range(int(capacity) + 1):
											student_entry = student_group.append('students', {})
											student_entry.update(males[0])
											practical_students.append(males[0])
											del males[0]
										student_group.save()
										# Practical:
										practical_student_group = frappe.get_doc('Student Group', student_group_name)
										if len(practical_students) % self.practical_capacity == 0: 
											practical_groups_size = len(practical_students) / self.practical_capacity
											if int(practical_groups_size) > 3:
												frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
											else:
												for i in range(int(practical_groups_size)):
													table_name = 'students' + str(i+1)
													for i in range(self.practical_capacity):
														student_entry = practical_student_group.append(table_name, {})
														student_entry.update(practical_students[0])
														del practical_students[0]
													practical_student_group.save()
										else:
											practical_groups_size = len(practical_students) / self.practical_capacity +1
											practical_capacity = len(practical_students) / int(practical_groups_size)
											if int(practical_groups_size) > 3:
												frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
											else:
												for j in range(int(practical_groups_size)):
													table_name = 'students' + str(j+1)
													if i < len(practical_students) % int(practical_groups_size):
														for i in range(int(practical_capacity) + 1):
															student_entry = practical_student_group.append(table_name, {})
															student_entry.update(practical_students[0])
															del practical_students[0]
														practical_student_group.save()
													else:
														for i in range(int(practical_capacity)):
															student_entry = practical_student_group.append(table_name, {})
															student_entry.update(practical_students[0])
															del practical_students[0]
														practical_student_group.save()
									else:
										student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(l+1) + ' Males'
										student_group = frappe.new_doc('Student Group')
										student_group.student_group_name = student_group_name
										student_group.batch = self.student_batch
										student_group.program = self.program
										student_group.group_based_on = self.based_on
										practical_students = []
										for i in range(int(capacity)):
											student_entry = student_group.append('students', {})
											student_entry.update(males[0])
											practical_students.append(males[0])
											del males[0]
										student_group.save()
										# Practical:
										practical_student_group = frappe.get_doc('Student Group', student_group_name)
										if len(practical_students) % self.practical_capacity == 0: 
											practical_groups_size = len(practical_students) / self.practical_capacity
											if int(practical_groups_size) > 3:
												frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
											else:
												for i in range(int(practical_groups_size)):
													table_name = 'students' + str(i+1)
													for i in range(self.practical_capacity):
														student_entry = practical_student_group.append(table_name, {})
														student_entry.update(practical_students[0])
														del practical_students[0]
													practical_student_group.save()
										else:
											practical_groups_size = len(practical_students) / self.practical_capacity +1
											practical_capacity = len(practical_students) / int(practical_groups_size)
											if int(practical_groups_size) > 3:
												frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
											else:
												for j in range(int(practical_groups_size)):
													table_name = 'students' + str(j+1)
													if i < len(practical_students) % int(practical_groups_size):
														for i in range(int(practical_capacity) + 1):
															student_entry = practical_student_group.append(table_name, {})
															student_entry.update(practical_students[0])
															del practical_students[0]
														practical_student_group.save()
													else:
														for i in range(int(practical_capacity)):
															student_entry = practical_student_group.append(table_name, {})
															student_entry.update(practical_students[0])
															del practical_students[0]
														practical_student_group.save()
								frappe.msgprint('Groups Successfully Generated...')
							# Females:
							if len(females) % self.capacity == 0:
								groups_size = len(females) / self.capacity
								for i in range(int(groups_size)):
									student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1) + ' Females'
									student_group = frappe.new_doc('Student Group')
									student_group.student_group_name = student_group_name
									student_group.batch = self.student_batch
									student_group.program = self.program
									student_group.group_based_on = self.based_on
									practical_students = []
									for i in range(self.capacity):
										student_entry = student_group.append('students', {})
										student_entry.update(females[0])
										practical_students.append(females[0])
										del females[0]
									student_group.save()
									# Practical:
									practical_student_group = frappe.get_doc('Student Group', student_group_name)
									if len(practical_students) % self.practical_capacity == 0: 
										practical_groups_size = len(practical_students) / self.practical_capacity
										if int(practical_groups_size) > 3:
											frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
										else:
											for i in range(int(practical_groups_size)):
												table_name = 'students' + str(i+1)
												for i in range(self.practical_capacity):
													student_entry = practical_student_group.append(table_name, {})
													student_entry.update(practical_students[0])
													del practical_students[0]
												practical_student_group.save()
									else:
										practical_groups_size = len(practical_students) / self.practical_capacity +1
										practical_capacity = len(practical_students) / int(practical_groups_size)
										if int(practical_groups_size) > 3:
											frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
										else:
											for j in range(int(practical_groups_size)):
												table_name = 'students' + str(j+1)
												if i < len(practical_students) % int(practical_groups_size):
													for i in range(int(practical_capacity) + 1):
														student_entry = practical_student_group.append(table_name, {})
														student_entry.update(practical_students[0])
														del practical_students[0]
													practical_student_group.save()
												else:
													for i in range(int(practical_capacity)):
														student_entry = practical_student_group.append(table_name, {})
														student_entry.update(practical_students[0])
														del practical_students[0]
													practical_student_group.save()
								frappe.msgprint('Groups Successfully Generated...')
							else:
								groups_size = len(females) / self.capacity + 1
								capacity = len(females) / int(groups_size)
								for n in range(int(groups_size)):
									if n < len(females) % int(groups_size):
										student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(n+1) + ' Females'
										student_group = frappe.new_doc('Student Group')
										student_group.student_group_name = student_group_name
										student_group.batch = self.student_batch
										student_group.program = self.program
										student_group.group_based_on = self.based_on
										practical_students = []
										for i in range(int(capacity) + 1):
											student_entry = student_group.append('students', {})
											student_entry.update(females[0])
											practical_students.append(females[0])
											del females[0]
										student_group.save()
										# Practical:
										practical_student_group = frappe.get_doc('Student Group', student_group_name)
										if len(practical_students) % self.practical_capacity == 0: 
											practical_groups_size = len(practical_students) / self.practical_capacity
											if int(practical_groups_size) > 3:
												frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
											else:
												for i in range(int(practical_groups_size)):
													table_name = 'students' + str(i+1)
													for i in range(self.practical_capacity):
														student_entry = practical_student_group.append(table_name, {})
														student_entry.update(practical_students[0])
														del practical_students[0]
													practical_student_group.save()
										else:
											practical_groups_size = len(practical_students) / self.practical_capacity +1
											practical_capacity = len(practical_students) / int(practical_groups_size)
											if int(practical_groups_size) > 3:
												frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
											else:
												for j in range(int(practical_groups_size)):
													table_name = 'students' + str(j+1)
													if i < len(practical_students) % int(practical_groups_size):
														for i in range(int(practical_capacity) + 1):
															student_entry = practical_student_group.append(table_name, {})
															student_entry.update(practical_students[0])
															del practical_students[0]
														practical_student_group.save()
													else:
														for i in range(int(practical_capacity)):
															student_entry = practical_student_group.append(table_name, {})
															student_entry.update(practical_students[0])
															del practical_students[0]
														practical_student_group.save()
									else:
										student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(n+1) + ' Females'
										student_group = frappe.new_doc('Student Group')
										student_group.student_group_name = student_group_name
										student_group.batch = self.student_batch
										student_group.program = self.program
										student_group.group_based_on = self.based_on
										practical_students = []
										for i in range(int(capacity)):
											student_entry = student_group.append('students', {})
											student_entry.update(females[0])
											practical_students.append(females[0])
											del females[0]
										student_group.save()
										# Practical:
										practical_student_group = frappe.get_doc('Student Group', student_group_name)
										if len(practical_students) % self.practical_capacity == 0: 
											practical_groups_size = len(practical_students) / self.practical_capacity
											if int(practical_groups_size) > 3:
												frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
											else:
												for i in range(int(practical_groups_size)):
													table_name = 'students' + str(i+1)
													for i in range(self.practical_capacity):
														student_entry = practical_student_group.append(table_name, {})
														student_entry.update(practical_students[0])
														del practical_students[0]
													practical_student_group.save()
										else:
											practical_groups_size = len(practical_students) / self.practical_capacity +1
											practical_capacity = len(practical_students) / int(practical_groups_size)
											if int(practical_groups_size) > 3:
												frappe.msgprint("Can't generate more then three Practical groups, please add more capacity to for the " + student_group_name + ' group and try again.')
											else:
												for j in range(int(practical_groups_size)):
													table_name = 'students' + str(j+1)
													if i < len(practical_students) % int(practical_groups_size):
														for i in range(int(practical_capacity) + 1):
															student_entry = practical_student_group.append(table_name, {})
															student_entry.update(practical_students[0])
															del practical_students[0]
														practical_student_group.save()
													else:
														for i in range(int(practical_capacity)):
															student_entry = practical_student_group.append(table_name, {})
															student_entry.update(practical_students[0])
															del practical_students[0]
														practical_student_group.save()
								frappe.msgprint('Groups Successfully Generated...')
		else:
			frappe.msgprint('please, get the students first...')	


	# This function is useless and can be deleted...
	@frappe.whitelist()
	def generate_groups(self):
		students = []
		for student in self.students:
			student_data = student.as_dict()
			students.append(student_data)

		keys = ['student_name', 'gender', 'program']
		cleaned_students = [{k: v for k, v in d.items() if k in keys} for d in students]

		if len(cleaned_students) > 0:
			if self.grouping_by == 'Theoretical':
				if self.based_on == 'All':
					if len(cleaned_students) <= self.capacity:
						student_group = frappe.new_doc('Student Group')
						student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G1'
						student_group.batch = self.student_batch
						student_group.program = self.program
						student_group.group_based_on = self.based_on
						for student in cleaned_students:
							student_entry = student_group.append('students', {})
							student_entry.update(student)
						student_group.save()
						frappe.msgprint('Groups Successfully Generated...')
					elif len(cleaned_students) > self.capacity and len(cleaned_students) <= self.capacity * 2:
						#frappe.msgprint('ssss')
						gSize = int(len(cleaned_students) / 2)
						if not len(cleaned_students) % 2 == 0:
							gSize = gSize + 1
							for i in range(2):
								#frappe.msgprint(str(cleaned_students[0]))
								student_group = frappe.new_doc('Student Group')
								student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1)
								student_group.batch = self.student_batch
								student_group.program = self.program
								student_group.group_based_on = self.based_on
								for i in range(gSize):
									student_entry = student_group.append('students', {})
									student_entry.update(cleaned_students[0])
									del cleaned_students[0]
								student_group.save()
								gSize = gSize -1
							frappe.msgprint('Groups Successfully Generated...')
						else:
							for i in range(2):
								#frappe.msgprint(str(cleaned_students[0]))
								student_group = frappe.new_doc('Student Group')
								student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1)
								student_group.batch = self.student_batch
								student_group.program = self.program
								student_group.group_based_on = self.based_on
								for i in range(gSize):
									student_entry = student_group.append('students', {})
									student_entry.update(cleaned_students[0])
									del cleaned_students[0]
								student_group.save()
							frappe.msgprint('Groups Successfully Generated...')

					elif len(cleaned_students) > self.capacity * 2 and len(cleaned_students) <= self.capacity * 3:
						#frappe.msgprint('ssss')
						gSize = int(len(cleaned_students) / 3)
						if not len(cleaned_students) % 3 == 0:
							if len(cleaned_students) % 3 == 1:
								gSize = gSize + 1
								for i in range(3):
									#frappe.msgprint(str(cleaned_students[0]))
									if i == 2:
										gSize = gSize + 1
									student_group = frappe.new_doc('Student Group')
									student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1)
									student_group.batch = self.student_batch
									student_group.program = self.program
									student_group.group_based_on = self.based_on
									for i in range(gSize):
										student_entry = student_group.append('students', {})
										student_entry.update(cleaned_students[0])
										del cleaned_students[0]
									student_group.save()
									gSize = gSize -1
								frappe.msgprint('Groups Successfully Generated...')
							elif len(cleaned_students) % 3 == 2:
								gSize = gSize + 2
								for i in range(3):
									if i == 2:
										gSize = gSize -1
									#frappe.msgprint(str(cleaned_students[0]))
									student_group = frappe.new_doc('Student Group')
									student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1)
									student_group.batch = self.student_batch
									student_group.program = self.program
									student_group.group_based_on = self.based_on
									for i in range(gSize):
										student_entry = student_group.append('students', {})
										student_entry.update(cleaned_students[0])
										del cleaned_students[0]
									student_group.save()
									gSize = gSize -1
								frappe.msgprint('Groups Successfully Generated...')
						else:
							for i in range(3):
								#frappe.msgprint(str(cleaned_students[0]))
								student_group = frappe.new_doc('Student Group')
								student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1)
								student_group.batch = self.student_batch
								student_group.program = self.program
								student_group.group_based_on = self.based_on
								for i in range(gSize):
									student_entry = student_group.append('students', {})
									student_entry.update(cleaned_students[0])
									del cleaned_students[0]
								student_group.save()
							frappe.msgprint('Groups Successfully Generated...')
					elif len(cleaned_students) > self.capacity * 3 and len(cleaned_students) <= self.capacity * 4:
						gSize = int(len(cleaned_students) / 4)
						if not len(cleaned_students) % 4 == 0:
							if len(cleaned_students) % 4 == 1:
								gSize = gSize + 2
								for i in range(4):
									#frappe.msgprint(str(cleaned_students[0]))
									if i == 3:
										gSize = gSize - 1
									student_group = frappe.new_doc('Student Group')
									student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1)
									student_group.batch = self.student_batch
									student_group.program = self.program
									student_group.group_based_on = self.based_on
									for i in range(gSize):
										student_entry = student_group.append('students', {})
										student_entry.update(cleaned_students[0])
										del cleaned_students[0]
									student_group.save()
									gSize = gSize -1
								frappe.msgprint('Groups Successfully Generated...')
							elif len(cleaned_students) % 4 == 2:
								gSize = gSize + 2
								for i in range(4):
									#frappe.msgprint(str(cleaned_students[0]))
									student_group = frappe.new_doc('Student Group')
									student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1)
									student_group.batch = self.student_batch
									student_group.program = self.program
									student_group.group_based_on = self.based_on
									for i in range(gSize):
										student_entry = student_group.append('students', {})
										student_entry.update(cleaned_students[0])
										del cleaned_students[0]
									student_group.save()
									gSize = gSize -1
								frappe.msgprint('Groups Successfully Generated...')
							elif len(cleaned_students) % 4 == 3:
								gSize = gSize + 2
								for i in range(4):
									#frappe.msgprint(str(cleaned_students[0]))
									if i == 3:
										gSize = gSize + 1
									student_group = frappe.new_doc('Student Group')
									student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1)
									student_group.batch = self.student_batch
									student_group.program = self.program
									student_group.group_based_on = self.based_on
									for i in range(gSize):
										student_entry = student_group.append('students', {})
										student_entry.update(cleaned_students[0])
										del cleaned_students[0]
									student_group.save()
									gSize = gSize -1
								frappe.msgprint('Groups Successfully Generated...')
						else:
							for i in range(4):
								#frappe.msgprint(str(cleaned_students[0]))
								student_group = frappe.new_doc('Student Group')
								student_group.student_group_name = self.student_batch + ' ' + self.program + ' ' + 'G' + str(i+1)
								student_group.batch = self.student_batch
								student_group.program = self.program
								student_group.group_based_on = self.based_on
								for i in range(gSize):
									student_entry = student_group.append('students', {})
									student_entry.update(cleaned_students[0])
									del cleaned_students[0]
								student_group.save()
							frappe.msgprint('Groups Successfully Generated...')
				elif self.based_on == 'By Sex':
					males = []
					females = []

					for student in cleaned_students:
						if student['gender'] == 'Male':
							males.append(student)
						elif student['gender'] == 'Female':
							females.append(student)

					if not males:
						self.based_on = 'All'
						frappe.msgprint('There are no Male students found, please set the Based On field to All.')
					elif not females:
						self.based_on = 'All'
						frappe.msgprint('There are no Female students found, please set the Based On field to All.')
					else :
						frappe.msgprint('start grouping here...')
					frappe.msgprint(str(males))
					frappe.msgprint(str(females))
			elif self.grouping_by == 'Practical':
				if len(cleaned_students) <= self.capacity:
						student_group = frappe.get_doc('Student Group', self.student_group)
						for student in cleaned_students:
							student_entry = student_group.append('students1', {})
							student_entry.update(student)
						student_group.save()
						frappe.msgprint('Practical Groups Successfully Generated...')
				elif len(cleaned_students) > self.capacity and len(cleaned_students) <= self.capacity * 2:
						#frappe.msgprint('ssss')
						gSize = int(len(cleaned_students) / 2)
						if not len(cleaned_students) % 2 == 0:
							gSize = gSize + 1
							for i in range(2):
								#frappe.msgprint(str(cleaned_students[0]))
								student_group = frappe.get_doc('Student Group', self.student_group)
								table_name = 'students' + str(i+1)
								for i in range(gSize): 
									student_entry = student_group.append(table_name, {})
									student_entry.update(cleaned_students[0])
									del cleaned_students[0]
								student_group.save()
								gSize = gSize -1
							frappe.msgprint('Practical Groups Successfully Generated...')
						else:
							for i in range(2):
								#frappe.msgprint(str(cleaned_students[0]))
								student_group = frappe.get_doc('Student Group', self.student_group)
								table_name = 'students' + str(i+1)
								for i in range(gSize):
									student_entry = student_group.append(table_name, {})
									student_entry.update(cleaned_students[0])
									del cleaned_students[0]
								student_group.save()
							frappe.msgprint('Practical Groups Successfully Generated...')
				elif len(cleaned_students) > self.capacity * 2 and len(cleaned_students) <= self.capacity * 3:
						#frappe.msgprint('ssss')
						gSize = int(len(cleaned_students) / 3)
						if not len(cleaned_students) % 3 == 0:
							if len(cleaned_students) % 3 == 1:
								gSize = gSize + 1
								for i in range(3):
									#frappe.msgprint(str(cleaned_students[0]))
									if i == 2:
										gSize = gSize + 1
									student_group = frappe.get_doc('Student Group', self.student_group)
									table_name = 'students' + str(i+1)
									for i in range(gSize):
										student_entry = student_group.append(table_name, {})
										student_entry.update(cleaned_students[0])
										del cleaned_students[0]
									student_group.save()
									gSize = gSize -1
								frappe.msgprint('Practical Groups Successfully Generated...')
							elif len(cleaned_students) % 3 == 2:
								gSize = gSize + 2
								for i in range(3):
									if i == 2:
										gSize = gSize -1
									#frappe.msgprint(str(cleaned_students[0]))
									student_group = frappe.get_doc('Student Group', self.student_group)
									table_name = 'students' + str(i+1)
									for i in range(gSize):
										student_entry = student_group.append(table_name, {})
										student_entry.update(cleaned_students[0])
										del cleaned_students[0]
									student_group.save()
									gSize = gSize -1
								frappe.msgprint('Practical Groups Successfully Generated...')
						else:
							for i in range(3):
								#frappe.msgprint(str(cleaned_students[0]))
								student_group = frappe.get_doc('Student Group', self.student_group)
								table_name = 'students' + str(i+1)
								for i in range(gSize):
									student_entry = student_group.append(table_name, {})
									student_entry.update(cleaned_students[0])
									del cleaned_students[0]
								student_group.save()
							frappe.msgprint('Practical Groups Successfully Generated...')
		else:
			frappe.msgprint('please, get the students first...')		
