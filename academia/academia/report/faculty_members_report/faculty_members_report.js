// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.query_reports["Faculty Members Report"] = {
	filters: [

		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: frappe.defaults.get_user_default("Company")
		},
		{
			label: __("Department"),
			fieldname: "department",
			fieldtype: "Link",
			options: "Department",
			get_query: () => ({
				filters: {
					company: frappe.query_report.get_filter_value("company"),
				},
			}),
		},
		{
			label: __("Date of Joining in University"),
			fieldname: "date_of_joining_in_university",
			fieldtype: "Date",
		},
		{
			label: __("Employment Type"),
			fieldname: "employment_type",
			fieldtype: "Link",
			options: "Employment Type",
		},
		{
			label: __("Academic Rank"),
			fieldname: "academic_rank",
			fieldtype: "Link",
			options: "Academic Rank",
		},
		{
			label: __("Scientific Degree"),
			fieldname: "scientific_degree_name",
			fieldtype: "Link",
			options: "Scientific Degree",
		},
	],
};
