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
		faculity: DF.Link
		grouping_by: DF.Literal["Theoretical", "Practical"]
		program: DF.Link
		student_batch: DF.Link
		student_group: DF.Link
		students: DF.Table[StudentGroupStudent]
		tolerance: DF.Int
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
			else:
				student_group = frappe.get_doc('Student Group', self.student_group)
				for student in student_group.students:
					student_data = student.as_dict()
					students.append(student_data)
		else:
			if not self.based_on:
				frappe.throw(_("Mandatory field - Based On"))
			elif not self.program:
				frappe.throw(_("Mandatory field - Program"))
			elif not self.student_batch:
				frappe.throw(_("Mandatory field - Student Batch"))
			elif not self.capacity:
				frappe.throw(_("Mandatory field - Capacity"))
			elif not self.tolerance:
				frappe.throw(_("Mandatory field - Tolerance"))
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
				frappe.msgprint('Practical here...')
		else:
			frappe.msgprint('please, get the students first...')		
