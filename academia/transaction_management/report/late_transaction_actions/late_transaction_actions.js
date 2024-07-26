// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.query_reports["Late Transaction Actions"] = {
	"filters": [
		{
            "fieldname": "filter_company",
            "label": "Company",
            "fieldtype": "Link",
            "options": "Company",
        },
		{
			"fieldname": "filter_department",
            "label": "Department",
            "fieldtype": "Link",
            "options": "Department"
		},
        {
			"fieldname": "filter_employee",
            "label": "Employee",
            "fieldtype": "Link",
            "options": "Employee",
		},
	] 
};
