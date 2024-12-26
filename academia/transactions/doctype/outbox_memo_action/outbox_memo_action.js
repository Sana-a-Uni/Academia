// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt
let mustInclude = [];

frappe.ui.form.on("Outbox Memo Action", {
	on_submit: function (frm) {
		frappe.call({
			method: "academia.transactions.doctype.outbox_memo.outbox_memo.update_share_permissions",
			args: {
				docname: frm.doc.outbox_memo,
				user: frappe.session.user,
				permissions: {
					read: 1,
					write: 0,
					share: 0,
					submit: 0,
				},
			},
			callback: function (response) {
				if (response.message) {
					outbox_memo_action_doc = frappe.get_doc("Outbox Memo Action", frm.doc.name);
					// frappe.db.set_value(inbox_memo , 'current_action_maker')
					frappe.db.set_value(
						"Outbox Memo",
						frm.doc.outbox_memo,
						"current_action_maker",
						outbox_memo_action_doc.recipients[0].recipient_email
					);
					// back to Transaction after save the transaction action
					frappe.set_route("Form", "Outbox Memo", frm.doc.outbox_memo);
					location.reload();
				}
			},
		});
	},

	refresh(frm) {
		if (frappe.session.user !== "Administrator" && frm.doc.docstatus == 0) {
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Employee",
					filters: { user_id: frappe.session.user },
				},
				callback: function (response) {
					const employee = response.message;
					if (employee) {
						// Set the values of the fields to those of the fetched employee record
						frm.set_value("start_from", employee.name);
						frm.set_value("from_company", employee.company);
						frm.set_value("from_department", employee.department);
						frm.set_value("from_designation", employee.designation);
					}
				},
			});
		}
		if (frm.doc.docstatus !== 0) {
			// 0 indicates "Draft" status
			frm.fields_dict.get_recipients.$wrapper.hide();
			frm.fields_dict.get_recipients.input.disabled = true;
			frm.fields_dict.clear_recipients.$wrapper.hide();
			frm.fields_dict.clear_recipients.input.disabled = true;
		}
	},

	before_save: function (frm) {
		// If the user is not an Administrator, set the created_by field to the current user
		if (frappe.session.user !== "Administrator") {
			frm.set_value("created_by", frappe.session.user);
		}
	},

	created_by: function (frm) {
		update_must_include(frm);
	},

	get_recipients: function (frm) {
		update_must_include(frm);
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
	if (frappe.session.user !== "Administrator") {
		frm.clear_table("recipients");
		frm.refresh_field("recipients");

		frappe.call({
			method: "frappe.client.get_value",
			args: {
				doctype: "Employee",
				fieldname: "name",
				filters: { user_id: frappe.session.user },
			},
			callback: function (response) {
				const employee_name = response.message.name;
				if (employee_name) {
					frappe.call({
						method: "academia.transactions.doctype.outbox_memo.outbox_memo.get_reports_to_hierarchy_reverse",
						args: {
							employee_name: employee_name,
						},
						callback: function (response) {
							mustInclude = response.message;
						},
					});
				}
			},
		});
	}
}
