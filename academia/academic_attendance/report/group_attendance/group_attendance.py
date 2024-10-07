# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

from typing import Dict, List, Optional, Tuple

import frappe
from frappe import _


Filters = frappe._dict

def execute(filters: Optional[Filters] = None):
	filters = frappe._dict(filters or {})
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns() -> List[Dict]:
	columns = []

	columns.extend(
		[
			{
				"label": _("Course"),
				"fieldname": "course",
				"fieldtype": "Link",
				"options": "Course Study",
				"width": 135,
			},
			{
				"label": _("Course Type"), 
				"fieldname": "course_type",
				"fieldtype": "Data", 
				"width": 120,
				"options": ["Theoretical","Practical"]
			},
			{
				"label": _("Instructor"),
				"fieldname": "instructor",
				"fieldtype": "Data",
				"options": "Faculty Member",
				"width": 200,
			},
			{
				"label": _("Total Absent"),
				"fieldname": "total_absent", 
				"fieldtype": "Float", 
				"width": 110
			},
			{
				"label": _("Total Present"),
				"fieldname": "total_present",
				"fieldtype": "Float",
				"width": 110,
			},
			{
				"label": _("Total Compensatory Lessons"),
				"fieldname": "total_compensatory_lesson",
				"fieldtype": "Float",
				"width": 120,
			}	
		]
	)

	return columns


def get_data(filters = None):
	data = []
	multi_group = []
	filters["docstatus"] = 1

	if filters.from_date and filters.to_date:
		filters["attendance_date"] = ["between", [filters.from_date,filters.to_date]]
		filters.pop("from_date")
		filters.pop("to_date")
	elif filters.from_date:
		filters["attendance_date"] = [">=", filters.from_date]
		filters.pop("from_date")
	elif filters.to_date:
		filters["attendance_date"] = ["<=", filters.to_date]
		filters.pop("to_date")

	Lesson_attendance = frappe.get_all(
	"Lesson Attendance", fields=["name","course", "course_type", "faculty_member", "faculty_member_name", "is_multi_group", "program", "level", "group"] ,filters = filters
	)
	
	if filters.program or filters.level or filters.group:
		Lesson_attendance_in = []
		filters_in = {"docstatus": 1}

		for field, value in {"faculty": filters.faculty, "academic_year":filters.academic_year, "academic_term":filters.academic_term,
					    "course":filters.course, "attendance_date": filters.attendance_date}.items():
			if value:
				filters_in[field] = value
		
		Lesson_attendance_in = frappe.get_all(
			"Lesson Attendance", fields=["name","course", "course_type","faculty_member", "faculty_member_name","is_multi_group", "program", "level", "group"],
			filters = filters_in
			)
		
		multi_gruop_filters = {"doctype": 'Multi Lesson Template' ,"parenttype": "Lesson Attendance","docstatus": 1}
		for field, value in {"program": filters.program, "level": filters.level, "group": filters.group}.items():
			if value:
				multi_gruop_filters[field] = value
		for record in Lesson_attendance_in:
				multi_gruop_filters['parent'] = record.name	
				exist = frappe.db.exists(multi_gruop_filters)
				if exist:
					
					multi_group.append(record)
	
	Lesson_attendance.extend(multi_group)
	temp = []
	for value in Lesson_attendance:
		value.pop("name")
		if value not in temp:
			temp.append(value)
	
	Lesson_attendance = temp
	for value in Lesson_attendance:
		filters["course"] = value["course"]
		filters["course_type"] = value["course_type"]
		filters["faculty_member"] = value["faculty_member"]
		row ={
			"course": value["course"],
			"course_type": value["course_type"],
			"instructor": value["faculty_member_name"],
			"total_absent": get_total(filters, "status", "Absent", value["is_multi_group"]),
			"total_present": get_total(filters, "status", "Present", value["is_multi_group"]),
			"total_compensatory_lesson": get_total(filters, "lesson_type", "Compensatory Lesson", value["is_multi_group"])
		}
		data.append(row)

	return data


def get_total(filters, field, value ,is_multi_group):
	count = 0
	filters[field] = value

	if is_multi_group:
		iner_filters = filters
		if filters.program:
			iner_filters.pop("program")
		if filters.level:
			iner_filters.pop("level")
		if filters.group:
			iner_filters.pop("group")

		multi_group_list = frappe.db.get_all("Lesson Attendance", pluck="name",filters=iner_filters)

		multi_group_filters = {"doctype": 'Multi Lesson Template' ,"parenttype": "Lesson Attendance"}
		for filter_field, value in {"program": filters.program, "level": filters.level, "group": filters.group}.items():
			if value:
				multi_group_filters[filter_field] = value

		for record in multi_group_list:
				multi_group_filters['parent'] = record
				exist = frappe.db.exists(multi_group_filters)
				if exist:
					count +=1
	else :
		count =frappe.db.count("Lesson Attendance", filters)

	filters.pop(field)

	return count
