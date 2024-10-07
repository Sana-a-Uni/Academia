# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns ()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns = []

	columns.extend(
		[
			{
				"label": _("Total Absent"),
				"fieldname": "total_absent", 
				"fieldtype": "Float", 
				"width": 130
			},
			{
				"label": _("Total Present"),
				"fieldname": "total_present",
				"fieldtype": "Float",
				"width": 130,
			},
			{
				"label": _("Total Compensatory Lessons"),
				"fieldname": "total_compensatory_lesson",
				"fieldtype": "Float",
				"width": 170,
			}	
		]
	)

	return columns


def get_data(filters = None):
	data = []
	row = {}
	total_absent = 0
	total_present = 0
	total_compensatory_lesson = 0
	multi_group_records = get_multi_group(filters)

	if multi_group_records:
		for value in multi_group_records:
			if value["status"] == "Present":
				total_present += 1
			elif value["status"] == "Absent":
				total_absent += 1
			if value["lesson_type"] == "Compensatory Lesson":
				total_compensatory_lesson += 1
			
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
		
	total_absent += get_total(filters, "status", "Absent")

	total_present += get_total(filters, "status", "Present")
	total_compensatory_lesson += get_total(filters, "lesson_type", "Compensatory Lesson")
	if total_absent or total_present or total_compensatory_lesson:
		row["total_absent"] = total_absent
		row["total_present"] = total_present
		row["total_compensatory_lesson"] = total_compensatory_lesson
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
    if filters.get("group"):
        conditions += "AND multi_group.group = %(group)s"
    if filters.get("from_date"):
        conditions += "AND attendance.attendance_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += "AND attendance.attendance_date <= %(to_date)s"

    query = f"""
        SELECT
            attendance.name as name,
            attendance.faculty_member,
            attendance.status,
		    attendance.lesson_type
        FROM
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

def get_total(filters, field, value):
	count = 0
	filters[field] = value
	
	count =frappe.db.count("Lesson Attendance", filters)
	filters.pop(field)
	
	return count
