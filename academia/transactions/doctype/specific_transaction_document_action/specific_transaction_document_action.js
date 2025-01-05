// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt
let mustInclude = [];
frappe.ui.form.on("Specific Transaction Document Action", {
	refresh(frm) {
		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "Specific Transaction Document",
				name: frm.doc.specific_transaction_document,
			},
			callback: function (response) {
				if (response.message) {
					const doc = response.message;

					// Check if the full_electronic field is checked
					if (!doc.full_electronic) {
						// Hide the "Submit" button
						frm.page.wrapper.find('.btn-primary[data-label="Submit"]').hide();

						// Add a custom submit button
						if (!frm.is_new() && frm.doc.docstatus === 0) {
							frm.add_custom_button(__("Submit"), function () {
								// Custom functionality
								custom_submit_functionality(frm);
							}).addClass("btn-primary");
						}
						y;
					}
				}
			},
		});

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
						frm.set_value("action_maker", employee.name);
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
					specific_transaction_document_action_doc = frappe.get_doc(
						"Specific Transaction Document Action",
						frm.doc.name
					);
					if (frm.doc.allow_recipient_to_redirect) {
						frappe.call({
							method: "academia.transactions.doctype.specific_transaction_document_action.specific_transaction_document_action.update_specific_transaction_document",
							args: {
								specific_transaction_document_name:
									frm.doc.specific_transaction_document, // Replace with the current document name
								current_action_maker:
									specific_transaction_document_action_doc.recipients[0]
										.recipient_email,
								allow_to_redirect: 1, // Uncheck the checkbox
							},
							callback: function (response) {
								if (!response.exc) {
									frappe.set_route(
										"Form",
										"Specific Transaction Document",
										frm.doc.specific_transaction_document
									);
									location.reload();
								} else {
									frappe.msgprint("There was an error!");
								}
							},
						});
					} else {
						frappe.call({
							method: "academia.transactions.doctype.specific_transaction_document_action.specific_transaction_document_action.update_specific_transaction_document",
							args: {
								specific_transaction_document_name:
									frm.doc.specific_transaction_document, // Replace with the current document name
								current_action_maker: "", // Set the desired value
								allow_to_redirect: 0, // Uncheck the checkbox
								status: "Completed", // Set status to "Complete"
							},
							callback: function (response) {
								if (!response.exc) {
									frappe.set_route(
										"Form",
										"Specific Transaction Document",
										frm.doc.specific_transaction_document
									);
									location.reload();
								} else {
									frappe.msgprint("There was an error!");
								}
							},
						});
					}
				}
			},
		});
	},
	before_save: function (frm) {
		// If the user is not an Administrator, set the created_by field to the current user
		if (frappe.session.user !== "Administrator") {
			frm.set_value("created_by", frappe.session.user);
		}
	},

	onload: function (frm) {
		if (frm.doc.docstatus == 0) {
			frm.set_value("action_date", frappe.datetime.now_date());
		}
		frm.get_field("recipients").grid.cannot_add_rows = true;
	},
	action_maker: function (frm) {
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
	if (frm.doc.action_maker) {
		frm.clear_table("recipients");
		frm.refresh_field("recipients");

		frappe.call({
			method: "academia.transactions.doctype.specific_transaction_document_action.specific_transaction_document_action.get_reports_to_hierarchy_reverse",
			args: {
				employee_name: frm.doc.action_maker,
			},
			callback: function (response) {
				mustInclude = response.message;
			},
		});
	}
}

function custom_submit_functionality(frm) {
	// Example custom functionality
	frappe.prompt(
		[
			{
				label: "Details",
				fieldname: "details",
				fieldtype: "Text",
			},
			{
				fieldname: "document_name",
				fieldtype: "Link",
				label: "Document Name",
				options: "Transaction",
				default: frm.doc.specific_transaction_document,
				read_only: 1,
				hidden: 1,
			},
			{
				fieldname: "start_employee",
				fieldtype: "Link",
				label: "Start From",
				options: "Employee",
				read_only: 1,
				hidden: 1,
				default: frm.doc.action_maker || "",
			},
			{
				fieldname: "end_employee",
				fieldtype: "Link",
				label: "End To",
				options: "Employee",
				default: frm.doc.recipients[0].recipient || "",
				read_only: 1,
				hidden: 1,
			},
			{
				fieldname: "through_middle_man",
				fieldtype: "Check",
				label: "Through Middle Man",
			},
			{
				fieldname: "middle_man",
				fieldtype: "Link",
				label: "Middle Man",
				options: "Employee",
				depends_on: "eval:doc.through_middle_man == 1",
				get_query: function () {
					return {
						query: "academia.transactions.doctype.outbox_memo.outbox_memo.get_middle_man_list",
					};
				},
			},
			{
				fieldname: "with_proof",
				label: __("With Proof"),
				fieldtype: "Check",
			},
			{
				fieldname: "proof",
				label: __("Proof"),
				fieldtype: "Attach",
				depends_on: "eval:doc.with_proof == 1",
			},
		],
		function (values) {
			if (values.through_middle_man && !values.middle_man) {
				frappe.msgprint({
					title: __("Error"),
					indicator: "red",
					message: __("Please select a Middle Man."),
				});
				return;
			}
			if (values.with_proof && !values.proof) {
				frappe.msgprint({
					title: __("Error"),
					indicator: "red",
					message: __("Please attach proof."),
				});
				return;
			}

			frappe.call({
				method: "academia.transactions.doctype.outbox_memo.outbox_memo.create_transaction_document_log",
				args: {
					start_employee: values.start_employee,
					end_employee: frm.doc.recipients[0].recipient,
					document_type: "Specific Transaction Document",
					document_name: values.document_name,
					document_action_type: "Specific Transaction Document Action",
					document_action_name: frm.doc.name,
					middle_man: values.middle_man,
					through_middle_man: values.through_middle_man ? "True" : "False",
					proof: values.proof,
					with_proof: values.with_proof ? "True" : "False",
				},
				callback: function (r) {
					if (r.message) {
						console.log("Transaction Document Log created:", r.message);
						if (r.message) {
							if (values.with_proof && !values.through_middle_man) {
								frappe.call({
									method: "academia.transactions.doctype.transaction_document_log.transaction_document_log.change_is_received",
									args: {
										doctype: "Specific Transaction Document",
										docname: frm.doc.specific_transaction_document,
										is_received: 1,
									},
									callback: function (r) {
										if (r.message) {
											frm.save("Submit");
											frm.events.on_submit(frm);
										}
									},
								});
							} else {
								frappe.call({
									method: "academia.transactions.doctype.transaction_document_log.transaction_document_log.change_is_received",
									args: {
										doctype: "Specific Transaction Document",
										docname: frm.doc.specific_transaction_document,
										is_received: 0,
									},
									callback: function (r) {
										if (r.message) {
											frm.save("Submit");
											frm.events.on_submit(frm);
										}
									},
								});
							}
							// location.reload();
						}
					}
				},
				error: function (r) {
					frappe.msgprint("You are in the error");
					console.error(r);
					frappe.msgprint({
						title: __("Error"),
						indicator: "red",
						message: r.message,
					});
				},
			});
		},
		__("Enter Approval Details"),
		__("Submit")
	);

	// Submit the document after the custom functionality
}
