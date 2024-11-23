// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Overtime Request", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Overtime Request", {
	validate: function (frm) {
		if (frm.doc.employees && frm.doc.default_shift && frm.doc.start_time && frm.doc.end_time) {
			// Loop through the child table of employees
			frm.doc.employees.forEach((employee_row) => {
				frappe.call({
					method: "frappe.client.insert",
					args: {
						doc: {
							doctype: "Shift Assignment",
							employee: employee_row.employee, // Access employee from child table
							shift_type: frm.doc.default_shift, // Assign selected shift
							start_date: frm.doc.start_time, // Overtime start time
							end_date: frm.doc.end_time, // Overtime end time
							company: employee_row.company, // Access Company from child table
						},
					},
					callback: function (response) {
						if (response.message) {
							frappe.msgprint(
								`Shift Assignment created for Employee: ${employee_row.employee}`
							);
						}
					},
					error: function (error) {
						frappe.msgprint(
							`Error creating Shift Assignment for Employee: ${employee_row.employee}`
						);
						console.error(error);
					},
				});
			});
		} else {
			frappe.msgprint(
				__(
					"Please fill all required fields: Employees, Default Shift, Start Time, and End Time."
				)
			);
		}
	},
});
