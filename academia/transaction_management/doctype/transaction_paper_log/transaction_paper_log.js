// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Transaction Paper Log", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Transaction Paper Log", {
	refresh: function (frm) {
		frm.disable_save();

		if (frm.doc.paper_progress == "Delivered to middle man") {
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Employee",
					fieldname: "user_id",
					filters: { name: frm.doc.middle_man },
				},
				callback: function (r) {
					if (r.message) {
						var middle_man_user_id = r.message.user_id;
						// Check if the current user is the same as the user of the end_employee
						if (frappe.session.user == middle_man_user_id) {
							// Add python function to give permission to End Employee to change the status to Received
							add_middle_man_received_action(frm);
						}
					}
				},
			});
		} else if (frm.doc.paper_progress == "Received by middle man") {
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Employee",
					fieldname: "user_id",
					filters: { name: frm.doc.middle_man },
				},
				callback: function (r) {
					if (r.message) {
						var middle_man_user_id = r.message.user_id;
						// Check if the current user is the same as the user of the end_employee
						if (frappe.session.user == middle_man_user_id) {
							add_middle_man_delivered_action(frm);
						}
					}
				},
			});
		} else if (frm.doc.paper_progress == "Delivered to end employee") {
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Employee",
					fieldname: "user_id",
					filters: { name: frm.doc.end_employee },
				},
				callback: function (r) {
					if (r.message) {
						var end_employee_user_id = r.message.user_id;
						// Check if the current user is the same as the user of the end_employee
						if (frappe.session.user == end_employee_user_id) {
							add_end_employee_received_action(frm);
						}
					}
				},
			});
		}
	},
});

function add_middle_man_received_action(frm) {
	cur_frm.page.add_action_item(__("Received"), function () {
		frappe.db.set_value(
			"Transaction Paper Log",
			frm.docname,
			"paper_progress",
			"Received by middle man"
		);
		location.reload();
	});
}

function add_middle_man_delivered_action(frm) {
	cur_frm.page.add_action_item(__("Delivered"), function () {
		frappe.db.set_value(
			"Transaction Paper Log",
			frm.docname,
			"paper_progress",
			"Delivered to end employee"
		);
		location.reload();
	});
}

function add_end_employee_received_action(frm) {
	cur_frm.page.add_action_item(__("Received"), function () {
		frappe.db.set_value(
			"Transaction Paper Log",
			frm.docname,
			"paper_progress",
			"Received by end employee"
		);
		location.reload();
	});
}
