# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import calendar
import json
import frappe
import os
from datetime import date
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, getdate
from frappe.utils.pdf import get_pdf


class LessonSchedulingTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		academic_program: DF.Literal["", "All Programs", "Specific Program"]
		group: DF.Link | None
		lesson_end_date: DF.Date
		lesson_start_date: DF.Date
		level: DF.Literal["", "All Levels", "Specific Level"]
		schedule_template: DF.ReadOnly | None
		schedule_template_version: DF.Link
		specific_level: DF.Link | None
		specific_program: DF.Link | None
	# end: auto-generated types
	pass


	@frappe.whitelist()
	def schedule_lesson(self):
		course_schedule = []
		course_schedule_error = []
		course_schedules = []
		course_schedules_errors = []
		rescheduled = []
		reschedule_errors = []
		multi_gruop_records = []
		cancelled_comcompensatory_lesson = []
		cancelled_comcompensatory_lessons = []
		groups = []

		self.validate_mandatory()
		self.validate_date()

		if self.specific_program or self.specific_level or self.group:
			is_multi_group_records = frappe.get_list(
				"Lesson Template", fields='*',filters={'schedule_template_version': self.schedule_template_version,
				'schedule_template': self.schedule_template,"is_multi_group": 1}
			)
			is_multi_group_records = self.validate_days(is_multi_group_records)

			multi_gruop_filters = {"doctype": 'Multi Lesson Template' ,"parenttype": "Lesson Template"}
			for field, value in {"program": self.specific_program, "level": self.specific_level, "group": self.group}.items():
				if value:
					multi_gruop_filters[field] = value

			for record in is_multi_group_records:
				multi_gruop_filters['parent'] = record.name	
				exist = frappe.db.exists(multi_gruop_filters)
				if exist:
					multi_gruop_records.append(record)
			cancelled_comcompensatory_lesson = self.delete_course_schedule_of_multi_group(
				rescheduled, reschedule_errors,cancelled_comcompensatory_lessons,is_multi_group_records[0]["faculty"]
				)
			
		filters = {'schedule_template_version': self.schedule_template_version, 'schedule_template':self.schedule_template}
		for field, value in {"program": self.specific_program, "level": self.specific_level,"group": self.group}.items():
			if value:
				filters[field] = value

		lesson_template = frappe.get_list(
			"Lesson Template", fields='*',filters=filters
		)
		lesson_template = self.validate_days(lesson_template)
		rescheduled, reschedule_errors, cancelled_comcompensatory_lessons = self.delete_course_schedule(
				rescheduled, reschedule_errors, cancelled_comcompensatory_lessons, lesson_template[0]['faculty']
			)
		
		if cancelled_comcompensatory_lesson:
			cancelled_comcompensatory_lessons.extend(cancelled_comcompensatory_lesson)
		
		if multi_gruop_records:
			lesson_template.extend(multi_gruop_records)

		for record in lesson_template:
			course_schedule, course_schedule_error, group = self.schedule_course(record['days'], record)
			course_schedules.extend(course_schedule)
			course_schedules_errors.extend(course_schedule_error)
			groups.extend(group)
			
		return dict(
			course_schedules=course_schedules,
			course_schedules_errors=course_schedules_errors,
			rescheduled=rescheduled,
			reschedule_errors=reschedule_errors,
			cancelled_comcompensatory_lessons=cancelled_comcompensatory_lessons,
			groups=groups
		)


	def validate_mandatory(self):
		"""Validates all mandatory fields"""
		fields = [
			"schedule_template_version",
			"lesson_start_date",
			"lesson_end_date",
		]  
		if self.academic_program == "Specific Program":
			fields.append("specific_program")
		if self.level == "Specific Level":
			fields.append("specific_level")
		

		for d in fields:
			if not self.get(d):
				frappe.throw(_("{0} is mandatory").format(self.meta.get_label(d)))


	def validate_date(self):
		"""Validates if Lesson Start Date is greater than Lesson End Date"""
		if self.lesson_start_date <  str(date.today()):
			frappe.throw(_("Lesson Start Date cannot be less than The date of today."))
		if self.lesson_start_date > self.lesson_end_date:
			frappe.throw(_("Lesson Start Date cannot be greater than Lesson End Date."))


	def validate_days(self, lesson_template):
		""" Validates the days """

		for record in lesson_template:
			days = []	
			if(record['saturday'] == 1):
				days.append("Saturday")

			if(record['sunday'] == 1):
				days.append("Sunday")
			
			if(record['monday'] == 1):
				days.append("Monday")
			
			if(record['tuesday'] == 1):
				days.append("Tuesday")
			
			if(record['wednesday'] == 1):
				days.append("Wednesday")
			
			if(record['thursday'] == 1):
				days.append("Thursday")

			if not days:
				frappe.throw(_("Please select at least one day in lesson templete <a href='/app/lesson-template/{}'>{}</a> to schedule the lesson.")
				 .format(record['name'],record['name']))
			else:
				record['days'] = days
		
		return lesson_template		


	def delete_course_schedule(self, rescheduled, reschedule_errors, cancelled_comcompensatory_lessons, faculty):
		"""Delete all Lesson schedule within the Date range and specified filters"""
		filters = [
				["faculty", "=", faculty],
				["date", ">=", self.lesson_start_date],
				["date", "<", self.lesson_end_date],
			]
		if self.specific_program:
			filters.append(["program", "=", self.specific_program])
		if self.specific_level:
			filters.append(["level", "=", self.specific_level])
		if self.group:
			filters.append(["group", "=",self.group])		
		
		schedules = frappe.get_list(
			"Lesson",
			fields=["name","lesson_type","compensatory_lesson_reference"],
			filters=filters,
		)

		for d in schedules:
			try:
				if(d.lesson_type == "Compensatory Lesson"):
						compensatory_lesson = frappe.get_doc('Compensatory Lesson', d.compensatory_lesson_reference)
						compensatory_lesson.db_set('cancelled_reason', "تعارض مع الجدول الجديد")
						compensatory_lesson.db_set('workflow_state','Cancelled')
						compensatory_lesson.cancel()
						cancelled_comcompensatory_lessons.append(compensatory_lesson)
				frappe.delete_doc("Lesson", d.name)
				rescheduled.append(d.name)
			except Exception:
				reschedule_errors.append(d.name)
		return rescheduled, reschedule_errors, cancelled_comcompensatory_lessons


	def delete_course_schedule_of_multi_group(self, rescheduled, reschedule_errors, cancelled_comcompensatory_lessons,faculty):
		"""Delete all Lesson schedule within the Date range and specified filters"""
		filters = [
				["faculty", "=", faculty],
				["is_multi_group", "=", 1],
				["date", ">=", self.lesson_start_date],
				["date", "<", self.lesson_end_date],
			]
	
		
		schedules = frappe.get_list(
			"Lesson",
			fields=["name","lesson_type","compensatory_lesson_reference"],
			filters=filters,
		)

		multi_gruop_filters = {"doctype": 'Multi Lesson Template' ,"parenttype": "Lesson"}
		for field, value in {"program": self.specific_program, "level": self.specific_level,"group": self.group}.items():
			if value:
				multi_gruop_filters[field] = value

		for d in schedules:
			multi_gruop_filters['parent'] = d.name	
			exist = frappe.db.exists(multi_gruop_filters)
			if exist:
				try:
					if(d.lesson_type == "Compensatory Lesson"):
						compensatory_lesson = frappe.get_doc('Compensatory Lesson', d.compensatory_lesson_reference)
						compensatory_lesson.db_set('cancelled_reason', "تعارض مع الجدول الجديد")
						compensatory_lesson.db_set('workflow_state','Cancelled')
						compensatory_lesson.cancel()
						cancelled_comcompensatory_lessons.append(compensatory_lesson)
					frappe.delete_doc("Lesson", d.name)
					rescheduled.append(d.name)
				except Exception:
					reschedule_errors.append(d.name)

		return cancelled_comcompensatory_lessons


	def schedule_course(self, days, lesson_template):
		"""Creates lesson schedules as per specified parameters"""
		course_schedules = []
		course_schedules_errors = []
		groups =[]

		date = self.lesson_start_date
		while date < self.lesson_end_date:
			if calendar.day_name[getdate(date).weekday()] in days:
				course_schedule = self.make_course_schedule(date, lesson_template)
				course_schedule.save()
				course_schedules_errors.append(date)
				group = self.create_multi_group(lesson_template, course_schedule.name)
				if group:
					groups.append(group)

				course_schedules.append(course_schedule)

			date = add_days(date, 1)

		return course_schedules, course_schedules_errors , groups


	def make_course_schedule(self, date, lesson_template):
		"""Makes a new Lesson Schedule.
		:param date: Date on which Course Lesson will be created."""
		lesson_schedule = frappe.new_doc("Lesson")
		lesson_schedule.schedule_template_version = lesson_template.schedule_template_version
		lesson_schedule.schedule_template = lesson_template.schedule_template
		lesson_schedule.is_multi_group = lesson_template.is_multi_group
		lesson_schedule.academic_year = lesson_template.academic_year
		lesson_schedule.academic_term = lesson_template.academic_term
		lesson_schedule.faculty = lesson_template.faculty
		lesson_schedule.program = lesson_template.program
		lesson_schedule.level = lesson_template.level
		lesson_schedule.lesson_type = lesson_template.lesson_type
		lesson_schedule.instructor = lesson_template.instructor
		lesson_schedule.group = lesson_template.group
		lesson_schedule.sub_group = lesson_template.sub_group
		lesson_schedule.room = lesson_template.room
		lesson_schedule.course_type = lesson_template.course_type
		lesson_schedule.course = lesson_template.course
		lesson_schedule.date = date
		lesson_schedule.from_time = lesson_template.from_time
		lesson_schedule.to_time = lesson_template.to_time
		
		return lesson_schedule
	

	def create_multi_group(self, lesson_template, parent):
		groups = {}
		if lesson_template.is_multi_group:
			multi_info = frappe.get_list('Multi Lesson Template',
											 parent_doctype = "Lesson Template", 
											 filters={'parent': lesson_template.name}, 
											 fields=["program" , "level", "group"], order_by='idx')
			
			for i in range(len(multi_info)):
				multi_group = frappe.get_doc(
					dict(
						doctype="Multi Lesson Template",
						parenttype= "Lesson",
						parent=parent,
						parentfield="table_hfgk",
						program= multi_info[i]["program"],
						level= multi_info[i]["level"],
						group= multi_info[i]["group"]
					)
				)
				multi_group.save()
				values = frappe.get_list('Multi Lesson Template',
													parent_doctype = "Lesson", 
													filters={'parent': parent}, 
													pluck="group", order_by='idx')
				groups["parent"] = parent
				groups["values"] = values
		return groups


	@frappe.whitelist()
	def get_filters_data(self):
		lesson_template = []
		programs = []
		levels = []
		groups = []
        
		filters = {'schedule_template_version': self.schedule_template_version, 'schedule_template': self.schedule_template}
		lesson_template = frappe.get_list(
			"Lesson Template", fields='*',filters=filters
		)

		multi_gruop_filters = {}
		for field, value in {"program": self.specific_program, "level": self.specific_level}.items():
				if value:
					multi_gruop_filters[field] = value

		for record in lesson_template:
			if record.is_multi_group:
				multi_gruop_filters ['parent'] = record.name
				multi_info = frappe.get_list('Multi Lesson Template',
												parent_doctype = "Lesson Template", 
												filters=multi_gruop_filters, 
												fields=["program" , "level", "group"], order_by='idx')
				for record in multi_info:
					programs.append(record["program"])
					levels.append(record["level"])
					groups.append(record["group"])

		for field, value in {"program": self.specific_program, "level": self.specific_level}.items():
			if value:
				filters[field] = value
		filters['is_multi_group'] = 0
		lesson_template = frappe.get_list(
			"Lesson Template", fields=["program" , "level", "group"],filters=filters
		)

		for record in lesson_template:
					programs.append(record["program"])
					levels.append(record["level"])
					groups.append(record["group"])
		programs = list(dict.fromkeys(programs))
		levels = list(dict.fromkeys(levels))
		groups = list(dict.fromkeys(groups))
		
		return {'programs': programs, 'levels':levels, 'groups':groups}


@frappe.whitelist()
def generate_pdf(cancelled_compensatory_lessons=None, file_name=None):
    try:        
        if not file_name:
            frappe.throw(_("File name is required."))
        
        if isinstance(cancelled_compensatory_lessons, str):
            try:
                cancelled_compensatory_lessons = json.loads(cancelled_compensatory_lessons)
            except json.JSONDecodeError:
                frappe.throw(_("Invalid JSON data for cancelled_compensatory_lessons."))
                
        data = cancelled_compensatory_lessons
        html =  frappe.render_template('templates/cancelled_compensatory_lesson.html', {'data': data})
                
        pdf = get_pdf(html)
        
        if pdf:            
            frappe.response['filename'] = f"{file_name}.pdf"
            frappe.response['filecontent'] = pdf
            frappe.response['type'] = "download"
            frappe.response['headers'] = {
                "Content-Type": "application/pdf",
                "Content-Disposition": f"attachment; filename={file_name}.pdf"
            }
        else:
            frappe.throw("An error occurred while generating the PDF.")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"PDF generation failed for file_name: {file_name}")
        frappe.throw(_("An error occurred while generating the PDF."))
		