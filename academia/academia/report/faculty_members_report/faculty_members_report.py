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
			"fieldtype": "Data",
			"fieldname": "faculty_member_name",
			"width": 200,
		},
		{
			"label": _("Company"),
			"fieldtype": "Link",
			"fieldname": "company",
			"width": 200,
			"options": "Company",
		},
		{
			"label": _("Department"),
			"fieldtype": "Link",
			"fieldname": "department",
			"width": 200,
			"options": "Department",
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
			"options": "Email"
		},
		{
			"label": _("Date of Joining in University"),
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
	# 	{
	# 		"label": _("Vin"),
	# 		"fieldname": "vin",
	# 		"fieldtype": "Link",
	# 		"options": "Customer Vehicles",
	# 		"width": 150,
	# 	},
	# 	{
	# 		"fieldname": "customer",
	# 		"label": _("customer"),
	# 		"fieldtype": "Link",
	# 		"options": "Customer",
	# 		"width": 100,
	# 	},
	# 	{"label": _("Description"), "fieldname": "description", "fieldtype": "Data", "width": 120},
	# 	{"label": _("Container No"), "fieldname": "container_no", "fieldtype": "Data", "width": 120},
	# 	{"label": _("Batch"), "fieldname": "batch", "fieldtype": "Data", "width": 120},
  
	# 	{"label": _("Buying Towing"), "fieldname": "buying_towing", "fieldtype": "Data", "width": 120},
	# 	{"label": _("Selling Towing"), "fieldname": "selling_towing", "fieldtype": "Data", "width": 120},
	# 	{"label": _("Gross Profit Towing"), "fieldname": "gross_profit_towing", "fieldtype": "Data", "width": 120},
	
	# 	{"label": _("Ocean Freight Price"), "fieldname": "buying_ocean_freight", "fieldtype": "Data", "width": 120},
	# 	{"label": _("Selling Ocean Freight"), "fieldname": "selling_ocean_freight", "fieldtype": "Data", "width": 120},
	# 	{"label": _("Gross Profit Ocean"), "fieldname": "gross_profit_ocean", "fieldtype": "Data", "width": 120},
  
  	# 	{"label": _("Buying Transit"), "fieldname": "buying_transit", "fieldtype": "Data", "width": 120},
	# 	{"label": _("Selling Transit"), "fieldname": "selling_transit", "fieldtype": "Data", "width": 120},
	# 	{"label": _("Gross Profit Transit"), "fieldname": "gross_profit_transit", "fieldtype": "Data", "width": 120},
	# ]
	return columns


# def get_columns() -> list[dict]:
	# return [
	# 	{
	# 		"label": _("Faculty"),
	# 		"fieldtype": "Link",
	# 		"fieldname": "faculty",
	# 		"width": 200,
	# 		"options": "faculty",
	# 	},
	# 	{
	# 		"label": _("Faculty Member Name"),
	# 		"fieldtype": "Data",
	# 		"fieldname": "faculty_member_name",
	# 		"width": 100,
	# 	},
	# 	{
	# 		"label": _("Employee Name"),
	# 		"fieldtype": "Dynamic Link",
	# 		"fieldname": "employee_name",
	# 		"width": 100,
	# 		"options": "employee",
	# 	},
	# 	{
	# 		"label": _("Email"),
	# 		"fieldtype": "Data",
	# 		"fieldname": "email",
	# 		"width": 150,
	# 		"options": "Email"
	# 	},
	# 	# {
	# 	# 	"label": _("New Leave(s) Allocated"),
	# 	# 	"fieldtype": "float",
	# 	# 	"fieldname": "leaves_allocated",
	# 	# 	"width": 200,
	# 	# },
	# 	# {
	# 	# 	"label": _("Leave(s) Taken"),
	# 	# 	"fieldtype": "float",
	# 	# 	"fieldname": "leaves_taken",
	# 	# 	"width": 150,
	# 	# },
	# 	# {
	# 	# 	"label": _("Leave(s) Expired"),
	# 	# 	"fieldtype": "float",
	# 	# 	"fieldname": "leaves_expired",
	# 	# 	"width": 150,
	# 	# },
	# 	# {
	# 	# 	"label": _("Closing Balance"),
	# 	# 	"fieldtype": "float",
	# 	# 	"fieldname": "closing_balance",
	# 	# 	"width": 150,
	# 	# },
	# ]


def get_data(filters):
    return frappe.db.sql(
        """
        SELECT
            `tabFaculty Member`.faculty_member_name,
            `tabFaculty Member`.company,
			`tabFaculty Member`.department,
            `tabFaculty Member`.email,
            `tabFaculty Member`.academic_rank,
            `tabFaculty Member`.scientific_degree,
            `tabFaculty Member`.date_of_joining_in_university,
			`tabFaculty Member`.employment_type
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

	if filters.get("employee"):
		conditions.append(" and `tabFaculty Member`.employee=%(employee)s")

	if filters.get("company"):
		conditions.append(" and `tabFaculty Member`.company=%(company)s")

	if filters.get("department"):
		conditions.append(" and `tabFaculty Member`.department=%(department)s")

	if filters.get("academic_rank"):
		conditions.append(" and `tabFaculty Member`.academic_rank=%(academic_rank)s")

	if filters.get("date_of_joining_in_university"):
		conditions.append(" and `tabFaculty Member`.date_of_joining_in_university=%(date_of_joining_in_university)s")
	

	if filters.get("employment_type"):
		conditions.append(" and `tabFaculty Member`.employment_type=%(employment_type)s")
	return " ".join(conditions) if conditions else ""
