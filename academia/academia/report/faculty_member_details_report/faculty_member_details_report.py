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
			"label": _("Faculty Member Name"),
			"fieldtype": "Link",
			"fieldname": "faculty_member_name",
			"options": "Faculty Member",
			# "width": 200,
		},
		{
			"label": _("Company"),
			"fieldtype": "Link",
			"fieldname": "company",
			"options": "Company",
			# "width": 150,

		},
		{
			"label": _("Department"),
			"fieldtype": "Link",
			"fieldname": "department",
			"options": "Department",
			# "width": 150,
		},
		{
			"label": _("Email"),
			"fieldtype": "Data",
			"fieldname": "email",
			"options": "Email",
			# "width": 200,

		},
		{
			"label": _("Employment Type"),
			"fieldtype": "Link",
			"fieldname": "employment_type",
			"options": "Employment Type",
			# "width": 100,
		},
		{
			"label": _("Date of Joining"),
			"fieldtype": "Date",
			"fieldname": "date_of_joining_in_university",
			# "width": 150,
		},
		{
			"label": _("Academic Rank"),
			"fieldtype": "Link",
			"fieldname": "academic_rank",
			"options": "Academic Rank",
			# "width": 150,
		},
		{
			"label": _("Scientific Degree"),
			"fieldtype": "Link",
			"fieldname": "scientific_degree",
			"options": "Scientific Degree",
			# "width": 150,
		},
		
	]
	return columns


def get_data(filters):
    return frappe.db.sql(
        """
        SELECT
            `tabFaculty Member`.faculty_member_name,
            `tabFaculty Member`.company,
			`tabFaculty Member`.department,
            `tabFaculty Member`.email,
			`tabFaculty Member`.employment_type,
            `tabFaculty Member`.date_of_joining_in_university,
            `tabFaculty Member`.academic_rank,
            `tabFaculty Member`.scientific_degree
        FROM
            `tabFaculty Member`
        WHERE
            `tabFaculty Member`.name IS NOT NULL {conditions}
        ORDER BY
            `tabFaculty Member`.faculty_member_name ASC """.format(
                conditions=get_conditions(filters)
            ),
        filters,
        as_dict=1,
    )


def get_conditions(filters):
	conditions = []

	if filters.get("name"):
		conditions.append(" and `tabFaculty Member`.name=%(name)s")

	if filters.get("company"):
		conditions.append(" and `tabFaculty Member`.company=%(company)s")

	if filters.get("department"):
		conditions.append(" and `tabFaculty Member`.department=%(department)s")

	if filters.get("academic_rank"):
		conditions.append(" and `tabFaculty Member`.academic_rank=%(academic_rank)s")

	if filters.get("scientific_degree"):
		conditions.append(" and `tabFaculty Member`.scientific_degree=%(scientific_degree)s")

	if filters.get("date_of_joining_in_university"):
		conditions.append(" and `tabFaculty Member`.date_of_joining_in_university=%(date_of_joining_in_university)s")
	
	if filters.get("email"):
		conditions.append(" and `tabFaculty Member`.email=%(email)s")
	
	if filters.get("employment_type"):
		conditions.append(" and `tabFaculty Member`.employment_type=%(employment_type)s")
	return " ".join(conditions) if conditions else ""
