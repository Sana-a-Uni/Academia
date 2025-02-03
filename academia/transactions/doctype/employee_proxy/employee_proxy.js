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
                    employee_company: frm.doc.employee_company,
                    employee_department: frm.doc.employee_department,
                    employee_designation: frm.doc.employee_designation,
                    name: ["!=", frm.doc.name] // Exclude the current record
                },
                fields: ["name"]
            },
            callback: function(response) {
                if (response.message.length > 0) {
                    console.log(response)
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
