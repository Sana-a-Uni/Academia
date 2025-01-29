// Copyright (c) 2025, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Proxy", {
	refresh(frm) {

	},
    before_save(frm) {
        frappe.call({
            method: "frappe.client.get_list",
            args: {
                doctype: "Employee Proxy",
                filters: {
                    company: frm.doc.company,
                    department: frm.doc.department,
                    designation: frm.doc.designation,
                    name: ["!=", frm.doc.name] // Exclude the current record
                },
                fields: ["name"]
            },
            callback: function(response) {
                if (response.message.length > 0) {
                    frappe.msgprint({
                        title: __('Error'),
                        indicator: 'red',
                        message: __("A record with the same Company, Department, and Designation already exists.")
                    });
                    frappe.validated = false;
                }
            }
        });
    }
});
