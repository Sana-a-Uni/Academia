// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.query_reports["Type of Transaction"] = {
	"filters": [
		{
            "fieldname": "filter_company",
            "label": "Company",
            "fieldtype": "Link",
            "options": "Company",
			"reqd": 1,
			// "default": get_default_company()
        },
		{
			"fieldname": "filter_department",
            "label": "Department",
            "fieldtype": "Link",
            "options": "Department"
		},
		{
            "fieldname": "filter_type",
            "label": "Type",
            "fieldtype": "Select",
            "options": ["outgoing", "incoming"],
            "default": "outgoing",
			"reqd": 1
        },
        
	]
};

function get_default_company() {
    var user = frappe.session.user;
    var company = "";
    frappe.db.get_value("Employee", { "user_id": user }, "company", function(r) {
        if (r.message && r.message.company) {
            company = r.message.company;
			console.log("company:", company)
        }
		else company = ""
    });
    return company;
}
