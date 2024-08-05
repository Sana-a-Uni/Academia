// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.query_reports["Group Attendance"] = {
	"filters": [
		{
			"fieldname":"faculty",
			"label": __("Faculty"),
			"fieldtype": "Link",
			"options": "Faculty",
			"reqd": 1,
		},
		{
			"fieldname":"academic_year",
			"label": __("Academic Year"),
			"fieldtype": "Link",
			"options": "Academic Year",
			"reqd": 1,
		},
		{
			"fieldname":"academic_term",
			"label": __("Academic Term"),
			"fieldtype": "Link",
			"options": "Academic Term",
			"reqd": 1,
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
			"reqd": 1,
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
			"fieldname":"course",
			"label": __("Course"),
			"fieldtype": "Link",
			"options": "Course Study",
			get_query: () => {
				var academic_year = frappe.query_report.get_filter_value('academic_year');
				var academic_term = frappe.query_report.get_filter_value('academic_term');
				var program = frappe.query_report.get_filter_value('program');
				var level = frappe.query_report.get_filter_value('level');
				
				return {
					filters: {
						'academic_year': academic_year,
						'academic_term': academic_term ,
						'program': program,
						'level': level
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
