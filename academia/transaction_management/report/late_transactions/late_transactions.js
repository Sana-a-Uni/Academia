// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.query_reports["Late Transactions"] = {
	"filters": [
		{
            "fieldname": "filter_company",
            "label": "Company",
            "fieldtype": "Link",
            "options": "Company",
			// "reqd": 1,
        },
		{
			"fieldname": "filter_department",
            "label": "Department",
            "fieldtype": "Link",
            "options": "Department",
			// "reqd": 1,
		}, 
	]
};
