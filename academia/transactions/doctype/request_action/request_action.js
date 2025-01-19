// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt
let mustInclude = [];

frappe.ui.form.on("Request Action", {
	before_save: function (frm) {
		frm.set_value("naming_series", frm.doc.request + "-ACT-");
	},
	on_submit: function (frm) {
		frappe.call({
			method: "academia.transactions.doctype.request.request.update_share_permissions",
			args: {
				docname: frm.doc.request,
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
					request_action_doc = frappe.get_doc("Request Action", frm.doc.name);
					// frappe.db.set_value(inbox_memo , 'current_action_maker')
					frappe.db.set_value(
						"Request",
						frm.doc.request,
						"current_action_maker",
						request_action_doc.recipients[0].recipient_email
					);
					// back to Transaction after save the transaction action
					frappe.set_route("Form", "Request", frm.doc.request);
					location.reload();
				}
			},
		});
	},
	refresh(frm) {
		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "Request",
				name: frm.doc.request,
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
						;
					}
				}
			},
		});

		// Hide 'add row' button
		frm.get_field("recipients").grid.cannot_add_rows = true;
		// Stop 'add below' & 'add above' options
		frm.get_field("recipients").grid.only_sortable();
		frm.refresh_field("recipients");

		if (frappe.session.user !== "Administrator" && frm.doc.docstatus == 0) {
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Employee",
					filters: {
						user_id: frappe.session.user,
					},
				},
				callback: function (response) {
					const employee = response.message;
					if (employee) {
						frm.set_value("action_maker", employee.name);
					}
				},
			});
		}
	},

	action_maker: function (frm) {
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
				if (selections.length > 1) {
					frappe.msgprint("You Can Only Select One Recipient");
					return;
				}
				// console.log(d.dialog.get_value("company"));
				// emptying Council members
				frm.set_value("recipients", []);
				// Hold employee names
				frappe.call({
					method: "frappe.client.get_list",
					args: {
						doctype: "Employee",
						filters: { name: ["in", selections], user_id: ["in", mustInclude] },
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

	onload: function (frm) {
		document.addEventListener("keydown", function (event) {
			// Check if the Ctrl + B combination is pressed
			if (event.ctrlKey && event.key === "b") {
				// Check if the current doctype is one of the specified doctypes
				if (frm.doctype === "Request Action") {
					// Prevent the default action and stop propagation
					event.preventDefault();
					event.stopPropagation();
					frappe.msgprint(__("The shortcut Ctrl + B is disabled for this doctype."));
				}
			}
		});
		const request = localStorage.getItem("request");

		// Set the transaction_reference field value if it exists
		if (request && frm.is_new()) {
			frm.set_value("request", request);
		}
		if (frm.doc.docstatus == 0) {
			frm.set_value("action_date", frappe.datetime.get_today());
			frm.set_value("created_by", frappe.session.user);
		}
	},
});

function update_must_include(frm) {
	if (frm.doc.action_maker) {
		frm.clear_table("recipients");
		frm.refresh_field("recipients");
		frappe.call({
			method: "academia.transactions.doctype.request_action.request_action.get_direct_reports_to_hierarchy_reverse",
			args: {
				employee_name: frm.doc.action_maker,
			},
			callback: function (response) {
				mustInclude = []
				if (response.message && response.message.length > 0) {
					// Filter out null values and employees without users
					mustInclude = response.message.filter(emp => emp !== null);
				}

				// If mustInclude is empty, add a placeholder value
				if (mustInclude.length === 0) {
					mustInclude.push({ name: "No valid employees", employee_name: "No valid employees" });
				}
				console.log(mustInclude);
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
				default: frm.doc.request,
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
					document_type: "Request",
					document_name: values.document_name,
					document_action_type: "Request Action",
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
										doctype: "Request",
										docname: frm.doc.request,
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
										doctype: "Request",
										docname: frm.doc.request,
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
