// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.query_reports["Group Attendance Summary"] = {
	"filters": [
		{
			"fieldname":"faculty",
			"label": __("Faculty"),
			"fieldtype": "Link",
			"options": "Faculty",
			"reqd": 1
		},
		{
			"fieldname":"academic_year",
			"label": __("Academic Year"),
			"fieldtype": "Link",
			"options": "Academic Year",
			"reqd": 1
		},
		{
			"fieldname":"academic_term",
			"label": __("Academic Term"),
			"fieldtype": "Link",
			"options": "Academic Term",
			"reqd": 1
		},
		{
			"fieldname":"program",
			"label": __("Program"),
			"fieldtype": "Link",
			"options": "Program Specification",
			"reqd": 1,
			get_query: () => {
				var faculty = frappe.query_report.get_filter_value('faculty');
				return {
					filters: {
						'faculty': faculty
					}
				};
			}
		},
		{
			"fieldname":"level",
			"label": __("Level"),
			"fieldtype": "Link",
			"options": "Level",
			"reqd": 1
		},
		{
			"fieldname":"group",
			"label": __("Group"),
			"fieldtype": "Link",
			"options": "Student Group",
			"reqd": 1,
			get_query: () => {
				var faculty = frappe.query_report.get_filter_value('faculty');
				var program = frappe.query_report.get_filter_value('program');
				return {
					filters: {
						'faculty': faculty,
						'program': program
					}
				};
			}
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date"
		}			
	]
};
