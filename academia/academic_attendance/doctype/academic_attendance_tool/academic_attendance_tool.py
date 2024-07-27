# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import datetime
import json
import frappe

from frappe.utils import time_diff_in_hours
from frappe.model.document import Document
from frappe.utils import getdate


class AcademicAttendanceTool(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		building: DF.Link | None
		company: DF.Link | None
		date: DF.Date | None
		faculty: DF.Link | None
		from_time: DF.Time | None
		late_entry: DF.Check
		late_entry_time: DF.Time | None
		note: DF.SmallText | None
		program: DF.Link | None
		room: DF.Link | None
		status: DF.Literal["", "Present", "Absent"]
		to_time: DF.Time | None
	# end: auto-generated types
	pass

@frappe.whitelist()
def get_employees(
	date: str | datetime.date, from_time: str | datetime.time = None, to_time: str | datetime.time = None, faculty: str = None,
	  academic_program: str = None, room : str =None
) -> dict[str, list]:
	
	filters = {"date": date}
	for field, value in {"from_time": from_time, "to_time": to_time, "faculty": faculty, "program": academic_program, "room":room}.items():
		if value:
			filters[field] = value


	employee_list = frappe.get_list(
	"Lesson", fields=["*"], filters=filters, order_by="instructor")

	# This code for get faculty member name
	for i in range(len(employee_list)):
		employee_id = employee_list[i]["instructor"]
		employee_name_list = frappe.get_list(
		"Faculty Member", fields=["faculty_member_name"],
		filters={"name":employee_id}, order_by="name")
		employee_list[i]["faculty_member_name"] = employee_name_list[0]["faculty_member_name"]
	
	# This code for get the inforation from Multi Lesson Template that is associated with lesson
	for i in range(len(employee_list)):
		if employee_list[i]["is_multi_group"]:
			employee_list[i]["multi_info"] = frappe.get_list('Multi Lesson Template',
											 parent_doctype = "Lesson", 
											 filters={'parent': employee_list[i]["name"]}, 
											 fields=["program" , "level", "group"])

	
	attendance_list = frappe.get_list(
	"Lesson Attendance",
	fields=["faculty_member", "faculty_member_name", "status", "lesson"],
	filters={
		"attendance_date": date,
		"docstatus": 1
	},
	order_by="faculty_member_name",
	)
	unmarked_attendance = _get_unmarked_attendance(employee_list, attendance_list)

	return {"marked": attendance_list, "unmarked": unmarked_attendance}


def _get_unmarked_attendance(employee_list: list[dict], attendance_list: list[dict]) -> list[dict]:
	marked_lesson=[entry.lesson for entry in attendance_list]
	unmarked_attendance = []

	for entry in employee_list:
		if entry.name not in marked_lesson:
			unmarked_attendance.append(entry)
				
	return unmarked_attendance


@frappe.whitelist()
def mark_employee_attendance(
	employee_list: list | str,
	status: str,
	date: str | datetime.date,
	leave_type: str = None,
	company: str = None,
	late_entry: int = None,
	late_entry_time = None,
	early_exit: int = None,
	early_exit_time = None,
	note: str = None,
) -> None:
	
	if isinstance(employee_list, str):
		employee_list = json.loads(employee_list)
	
	for employee in employee_list:	
		lesson = frappe.get_doc('Lesson', employee)
		if status == "Present":
			teaching_hours = time_diff_in_hours(lesson.to_time, lesson.from_time)
		else :
			teaching_hours = 0
		
		attendance = frappe.get_doc(
			dict(
				doctype="Lesson Attendance",
				schedule_template_version=lesson.schedule_template_version,
				schedule_template=lesson.schedule_template,
				course_type=lesson.course_type,
				subgroup=lesson.sub_group,
				is_multi_group=lesson.is_multi_group,
				academic_year=lesson.academic_year,
				academic_term=lesson.academic_term,
				faculty=lesson.faculty,
				program=lesson.program,
				level=lesson.level,
				lesson_type=lesson.lesson_type,
				faculty_member=lesson.instructor,
				course=lesson.course,
				room=lesson.room,
				group=lesson.group,
				attendance_date=getdate(date),
				from_time=lesson.from_time,
				to_time=lesson.to_time,
				status=status,
				late_entry=late_entry,
				late_entry_time=late_entry_time,
				early_exit=early_exit,
				early_exit_time=early_exit_time,
				late_entry_note=note,
				teaching_hours = teaching_hours,
				lesson=employee
			)
		)
		attendance.insert()
		attendance.submit()

		if lesson.is_multi_group:
			multi_info = frappe.get_list('Multi Lesson Template',
											 parent_doctype = "Lesson", 
											 filters={'parent': employee}, 
											 fields=["program" , "level", "group"])
			for info in multi_info:
				multi_group = frappe.get_doc(
					dict(
						doctype="Multi Lesson Template",
						parenttype= "Lesson Attendance",
						parent=attendance.name,
						parentfield="multi_groups",
						program= info["program"],
						level= info["level"],
						group= info["group"]
					)
				)
				multi_group.insert()
				multi_group.submit()
