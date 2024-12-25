// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt
let mustInclude = [];

frappe.ui.form.on("Outbox Memo", {
	before_submit: function (frm) {
		if (frm.doc.type === "Internal" && frm.doc.direction != "Downward") {
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Employee",
					filters: { name: frm.doc.start_from },
					fieldname: "reports_to",
				},
				callback: function (response) {
					if (response.message) {
						reports_to = response.message.reports_to;
						frappe.call({
							method: "frappe.client.get_value",
							args: {
								doctype: "Employee",
								filters: { name: reports_to },
								fieldname: "user_id",
							},
							callback: function (response) {
								if (response.message) {
									user_id = response.message.user_id;
									frm.set_value("current_action_maker", user_id);
								}
							},
						});
					}
				},
			});
		} else if (frm.doc.type === "Internal" && frm.doc.direction === "Downward") {
			frm.set_value("current_action_maker", frm.doc.recipients[0].recipient_email);
		} else {
			console.log("External");
		}
	},

	refresh(frm) {
		if (frm.doc.current_action_maker === frappe.session.user) {
			add_approve_action(frm);
			add_reject_action(frm);
			// add_reject_action(frm);
		}
	},

	onload: function (frm) {
		if (!frm.doc.start_from) {
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Employee",
					filters: { user_id: frappe.session.user },
					fieldname: "name",
				},
				callback: function (response) {
					if (response.message) {
						frm.set_value("start_from", response.message.name);
					}
				},
			});
		}
	},

	start_from: function (frm) {
		update_must_include(frm);
	},

	direction: function (frm) {
		update_must_include(frm);
	},

	get_recipients: function (frm) {
		let setters = {
			employee_name: null,
			department: null,
			designation: null,
		};

		new frappe.ui.form.MultiSelectDialog({
			doctype: "Employee",
			target: frm,
			setters: setters,

			// add_filters_group: 1,
			// date_field: "transaction_date",
			get_query() {
				let filters = {
					docstatus: ["!=", 2],
					user_id: ["in", mustInclude],
				};
				if (frm.doc.type == "External") {
					filters.company = this.setters.company || "";
				}
				return {
					filters: filters,
				};
			},
			primary_action_label: __("Get Recipients"),

			action(selections) {
				// console.log(d.dialog.get_value("company"));
				// emptying Council members
				frm.set_value("recipients", []);
				// Hold employee names
				frappe.call({
					method: "frappe.client.get_list",
					args: {
						doctype: "Employee",
						filters: { name: ["in", selections] },
						fields: [
							"name",
							"employee_name",
							"designation",
							"department",
							"company",
							"user_id",
						],
					},
					callback: (response) => {
						var selectedEmployees = response.message;

						// frm.set_value('recipients', []);

						selectedEmployees.forEach((employee) => {
							frm.add_child("recipients", {
								recipient: employee.name, // Use document name instead of employee_name
								recipient_name: employee.employee_name,
								recipient_company: employee.company,
								recipient_department: employee.department,
								recipient_designation: employee.designation,
								recipient_email: employee.user_id,
							});
						});

						this.dialog.hide();

						frm.refresh_field("recipients");

						// // Hide the "Add" button for the recipients table if through_route is checked and there's a recipient
						// frm.get_field("recipients").grid.grid_buttons.find(".grid-add-row").toggle(!frm.doc.through_route || existingRecipients.length === 0);
					},
				});
			},
		});
	},

	clear_recipients: function (frm) {
		frm.clear_table("recipients");
		frm.refresh_field("recipients");
	},
});

function update_must_include(frm) {
	if (frm.doc.start_from) {
		frm.clear_table("recipients");
		frm.refresh_field("recipients");

		if (frm.doc.type === "External") {
			frappe.call({
				method: "academia.transactions.doctype.outbox_memo.outbox_memo.get_all_employees_except_start_from_company",
				args: {
					start_from_company: frm.doc.start_from_company,
				},
				callback: function (response) {
					mustInclude = response.message;
				},
			});
		} else if (frm.doc.type === "Internal" && frm.doc.direction !== "Downward") {
			frappe.call({
				method: "academia.transactions.doctype.outbox_memo.outbox_memo.get_reports_to_hierarchy",
				args: {
					employee_name: frm.doc.start_from,
				},
				callback: function (response) {
					mustInclude = response.message;
				},
			});
		} else {
			frappe.call({
				method: "academia.transactions.doctype.outbox_memo.outbox_memo.get_reports_to_hierarchy_reverse",
				args: {
					employee_name: frm.doc.start_from,
				},
				callback: function (response) {
					mustInclude = response.message;
				},
			});
		}
	}
}

function add_approve_action(frm) {
	cur_frm.page.add_action_item(__("Approve"), function () {
		frappe.prompt(
			[
				{
					label: "Details",
					fieldname: "details",
					fieldtype: "Text",
				},
			],
			function (values) {
				frappe.call({
					method: "academia.transactions.doctype.outbox_memo.outbox_memo.create_new_outbox_memo_action",
					args: {
						user_id: frappe.session.user,
						outbox_memo: frm.doc.name,
						type: "Approved",
						details: values.details || "",
					},
					callback: function (r) {
						if (r.message) {
							// console.log(r.message);
							if (r.message) {
								frappe.db
									.set_value(
										"Outbox Memo",
										frm.docname,
										"current_action_maker",
										r.message.action_maker
									)
									.then(() => {
										location.reload();
									});
							}
							// frappe.db.set_value('Transaction', frm.docname, 'status', 'Approved');
						}
					},
				});
			},
			__("Enter Approval Details"),
			__("Submit")
		);
	});
}

function add_reject_action(frm) {
	cur_frm.page.add_action_item(__("Reject"), function () {
		frappe.prompt(
			[
				{
					label: "Details",
					fieldname: "details",
					fieldtype: "Text",
				},
			],
			function (values) {
				frappe.call({
					method: "academia.transactions.doctype.outbox_memo.outbox_memo.create_new_outbox_memo_action",
					args: {
						user_id: frappe.session.user,
						outbox_memo: frm.doc.name,
						type: "Rejected",
						details: values.details || "",
					},
					callback: function (r) {
						if (r.message) {
							location.reload();
							// frappe.db.set_value('Transaction', frm.docname, 'status', 'Rejected');
						}
					},
				});
			},
			__("Enter Rejection Details"),
			__("Submit")
		);
	});
}

function add_reject_action(frm) {
	cur_frm.page.add_action_item(__("Reject"), function () {
		frappe.prompt(
			[
				{
					label: "Details",
					fieldname: "details",
					fieldtype: "Text",
				},
			],
			function (values) {
				frappe.call({
					method: "academia.transactions.doctype.outbox_memo.outbox_memo.create_new_outbox_memo_action",
					args: {
						user_id: frappe.session.user,
						outbox_memo: frm.doc.name,
						type: "Rejected",
						details: values.details || "",
						inbox_from: frm.doc.inbox_from || "",
					},
					callback: function (r) {
						if (r.message) {
							location.reload();
							// frappe.db.set_value('Transaction', frm.docname, 'status', 'Rejected');
						}
					},
				});
			},
			__("Enter Rejection Details"),
			__("Submit")
		);
	});
}
