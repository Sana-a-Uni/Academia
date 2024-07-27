// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.query_reports["External Transactions By Type"] = {
	"filters": [
		{
            "fieldname": "filter_type",
            "label": "Type",
            "fieldtype": "Select",
            "options": ["Outgoing", "Incoming"],
            "default": "outgoing",
			"reqd": 1
        },
	]
};
