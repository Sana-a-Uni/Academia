# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{
			"label": _("Faculty"),
			"fieldtype": "Link",
			"fieldname": "faculty",
			"width": 200,
			"options": "Company",
		},
		{
			"label": _("Faculty Member Name"),
			"fieldtype": "Data",
			"fieldname": "faculty_member_name",
			"width": 200,
		},
		{
			"label": _("Employment Type"),
			"fieldtype": "Link",
			"fieldname": "employment_type",
			"width": 100,
			"options": "Employment Type",
		},
		{
			"label": _("Email"),
			"fieldtype": "Data",
			"fieldname": "email",
			"width": 200,
		},
		{
			"label": _("Date of Joining"),
			"fieldtype": "Date",
			"fieldname": "date_of_joining_in_university",
			"width": 150
		},
		{
			"label": _("Academic Rank"),
			"fieldtype": "Link",
			"fieldname": "academic_rank",
			"width": 150,
			"options": "Academic Rank"
		},
		{
			"label": _("Scientific Degree"),
			"fieldtype": "Link",
			"fieldname": "scientific_degree",
			"width": 150,
			"options": "Scientific Degree"
		},
	]
	return columns

def get_data(filters):
	return frappe.db.sql(
		"""
		SELECT
			`tabFaculty Member`.faculty_member_name,
			`tabFaculty Member`.academic_rank,
			`tabFaculty Member`.company as faculty,
			`tabFaculty Member`.email,
			`tabFaculty Member`.scientific_degree,
			`tabFaculty Member`.date_of_joining_in_university,
			`tabFaculty Member`.employment_type
		FROM
			`tabFaculty Member`
		WHERE
			`tabFaculty Member`.name IS NOT NULL {conditions}
		ORDER BY
			`tabFaculty Member`.creation ASC
		""".format(conditions=get_conditions(filters)),
		filters,
		as_dict=1,
	)

def get_conditions(filters):
	conditions = []

	if filters.get("employee"):
		conditions.append(" and `tabFaculty Member`.employee=%(employee)s")

	if filters.get("department"):
		conditions.append(" and `tabFaculty Member`.department=%(department)s")

	if filters.get("academic_rank"):
		conditions.append(" and `tabFaculty Member`.academic_rank=%(academic_rank)s")

	if filters.get("date_of_joining_in_university"):
		conditions.append(" and `tabFaculty Member`.date_of_joining_in_university=%(date_of_joining_in_university)s")
	
	if filters.get("employment_type"):
		conditions.append(" and `tabFaculty Member`.employment_type=%(employment_type)s")

	return " ".join(conditions) if conditions else ""
