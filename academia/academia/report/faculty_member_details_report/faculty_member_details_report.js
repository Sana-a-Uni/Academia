// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.query_reports["Faculty Member Details Report"] = {
	filters: [
	// 	{
	// 		fieldname: "from_date",
	// 		label: __("From Date"),
	// 		fieldtype: "Date",
	// 		reqd: 1,
	// 		default: frappe.defaults.get_default("year_start_date")
	// 	},
	// 	{
	// 		fieldname: "to_date",
	// 		label: __("To Date"),
	// 		fieldtype: "Date",
	// 		reqd: 1,
	// 		default: frappe.defaults.get_default("year_end_date")
	// 	},
		{
			label: __("Faculty"),
			fieldname: "faculty",
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: frappe.defaults.get_user_default("Company")
		},
		{
			label: __("Employee"),
			fieldname: "employee",
			fieldtype: "Link",
			options: "Employee",
		},
		// {
		// 	label: __("Employment Type"),
		// 	fieldname: "employment_type",
		// 	fieldtype: "Link",
		// 	options: "Employment Type",
		// },
		// {
		// 	fieldname: "academic_rank",
		// 	label: __("Academic Rank"),
		// 	fieldtype: "Link",
		// 	options: "Academic Rank",
		// },
		{
			fieldname: "employee_status",
			label: __("Employee Status"),
			fieldtype: "Select",
			options: [
				"",
				{ "value": "Active", "label": __("Active") },
				{ "value": "Inactive", "label": __("Inactive") },
				{ "value": "Suspended", "label": __("Suspended") },
				{ "value": "Left", "label": __("Left") },
			],
			default: "Active",
		},
		// {
		// 	fieldname: "consolidate_leave_types",
		// 	label: __("Consolidate Leave Types"),
		// 	fieldtype: "Check",
		// 	default: 1,
		// 	depends_on: "eval: !doc.employee",
		// }
	],
};
