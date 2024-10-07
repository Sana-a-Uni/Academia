# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from typing import Dict, List, Optional, Tuple

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns() -> List[Dict]:
	columns = []

	columns.extend(
		[
			{
				"label": _("Attendance Date"), 
				"fieldname": "attendance_date",
				"fieldtype": "date", 
				"width": 115,
			},
			{
				"label": _("Time"),
				"fieldname": "time",
				"fieldtype": "Data",
				"width": 160,
			},
			{
				"label": _("Status"),
				"fieldname": "status",
				"fieldtype": "select",
				"options": ["Present","Absent"],
				"width": 200,
			},
			{
				"label": _("Late Entry"),
				"fieldname": "late_entry", 
				"fieldtype": "Check", 
				"width": 110
			},
			{
				"label": _("Early Exit"),
				"fieldname": "early_exit", 
				"fieldtype": "Check", 
				"width": 110
			},
			{
				"label": _("Note"),
				"fieldname": "note",
				"fieldtype": "Small Text",
				"width": 110,
			}
		]
	)

	return columns


def get_data(filters = None, pdf = None, from_date = None, to_date = None):
	data = []
	row = {}
	multi_group_records = []
	lesson_attendance_list = []
	multi_group_records = get_multi_group(filters)
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

	lesson_attendance_list = frappe.get_all("Lesson Attendance", fields=['*'] ,filters = filters)
	lesson_attendance_list.extend(multi_group_records)

	for lessson in lesson_attendance_list:
		time = str(lessson["from_time"]) + "-" + str(lessson["to_time"])
		row ={
			"attendance_date": lessson["attendance_date"],
			"time": time ,
			"status": lessson["status"],
			"late_entry": lessson['late_entry'],
			"early_exit": lessson['late_entry'],
			"note": lessson['late_entry_note']
		}
		data.append(row)

	return data


def get_multi_group(filters):
    conditions = ""
    if filters.get("faculty"):
        conditions += "AND attendance.faculty = %(faculty)s"
    if filters.get("academic_year"):
        conditions += "AND attendance.academic_year = %(academic_year)s"
    if filters.get("academic_term"):
        conditions += "AND attendance.academic_term = %(academic_term)s"
    if filters.get("program"):
        conditions += "AND multi_group.program = %(program)s"
    if filters.get("level"):
        conditions += "AND multi_group.level = %(level)s"
    if filters.get("faculty_member"):
        conditions += "AND attendance.faculty_member = %(faculty_member)s"
    if filters.get("course"):
        conditions += "AND attendance.course = %(course)s"
    if filters.get("group"):
        conditions += "AND multi_group.group = %(group)s"
    if filters.get("from_date"):
        conditions += "AND attendance.attendance_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += "AND attendance.attendance_date <= %(to_date)s"

    query = f"""
        SELECT * FROM
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