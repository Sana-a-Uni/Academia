// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt
let mustInclude = [];
frappe.ui.form.on("Specific Transaction Document Action", {
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
	on_submit: function (frm) {
		frappe.call({
			method: "academia.transactions.doctype.specific_transaction_document.specific_transaction_document.update_share_permissions",
			args: {
				docname: frm.doc.specific_transaction_document,
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
					specific_transaction_document_action_doc = frappe.get_doc("Specific Transaction Document Action", frm.doc.name);
					// frappe.db.set_value(inbox_memo , 'current_action_maker')
					if(frm.doc.allow_recipient_to_redirect){
						frappe.call({
							method: "academia.transactions.doctype.specific_transaction_document_action.specific_transaction_document_action.update_specific_transaction_document",
							args: {
								specific_transaction_document_name: frm.doc.specific_transaction_document,  // Replace with the current document name
								current_action_maker: specific_transaction_document_action_doc.recipients[0].recipient_email,
								allow_to_redirect: 1,            // Uncheck the checkbox
							},
							callback: function(response) {
								if (!response.exc) {
									frappe.set_route("Form", "Specific Transaction Document", frm.doc.specific_transaction_document)
									location.reload();
								} else {
									frappe.msgprint("There was an error!")
								}
							}
						});		
					}
					else {
						frappe.call({
							method: "academia.transactions.doctype.specific_transaction_document_action.specific_transaction_document_action.update_specific_transaction_document",
							args: {
								specific_transaction_document_name: frm.doc.specific_transaction_document,  // Replace with the current document name
								current_action_maker: "",        // Set the desired value
								allow_to_redirect: 0,            // Uncheck the checkbox
								status: "Completed"               // Set status to "Complete"
							},
							callback: function(response) {
								if (!response.exc) {
									frappe.set_route("Form", "Specific Transaction Document", frm.doc.specific_transaction_document)
									location.reload();
								} else {
									frappe.msgprint("There was an error!")
								}
							}
						});						
					}
				}
			},
		});
	},

	onload: function(frm) {

        frm.get_field('recipients').grid.cannot_add_rows = true;
    },
    start_from: function (frm) {
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

		frappe.call({
            method: "academia.transactions.doctype.specific_transaction_document_action.specific_transaction_document_action.get_reports_to_hierarchy_reverse",
            args: {
                employee_name: frm.doc.start_from,
            },
            callback: function (response) {
                mustInclude = response.message;
            },
        });
	}
}