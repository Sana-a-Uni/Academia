// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt
let mustInclude = [];

frappe.ui.form.on("Outbox Memo Action", {
	before_submit: function (frm) {
		// frappe.prompt(
		// 	[
		// 		{
		// 			label: "Details",
		// 			fieldname: "details",
		// 			fieldtype: "Text",
		// 		},
		// 		{
		// 			fieldname: "document_name",
		// 			fieldtype: "Link",
		// 			label: "Document Name",
		// 			options: "Transaction",
		// 			default: frm.doc.outbox_memo,
		// 			read_only: 1,
		// 			hidden: 1,
		// 		},
		// 		{
		// 			fieldname: "start_employee",
		// 			fieldtype: "Link",
		// 			label: "Start From",
		// 			options: "Employee",
		// 			read_only: 1,
		// 			hidden: 1,
		// 			default: frm.doc.action_maker || "",
		// 		},
		// 		{
		// 			fieldname: "end_employee",
		// 			fieldtype: "Link",
		// 			label: "End To",
		// 			options: "Employee",
		// 			default: frm.doc.recipients[0].recipient || "",
		// 			read_only: 1,
		// 			hidden: 1,
		// 		},
		// 		{
		// 			fieldname: "through_middle_man",
		// 			fieldtype: "Check",
		// 			label: "Through Middle Man",
		// 		},
		// 		{
		// 			fieldname: "middle_man",
		// 			fieldtype: "Link",
		// 			label: "Middle Man",
		// 			options: "Employee",
		// 			depends_on: "eval:doc.through_middle_man == 1",
		// 			get_query: function () {
		// 				return {
		// 					query: "academia.transactions.doctype.outbox_memo.outbox_memo.get_middle_man_list",
		// 				};
		// 			},
		// 		},
		// 		{
		// 			fieldname: "with_proof",
		// 			label: __("With Proof"),
		// 			fieldtype: "Check",
		// 		},
		// 		{
		// 			fieldname: "proof",
		// 			label: __("Proof"),
		// 			fieldtype: "Attach",
		// 			depends_on: "eval:doc.with_proof == 1",
		// 		},
		// 	],
		// 	function (values) {
		// 		if (values.through_middle_man && !values.middle_man) {
		// 			frappe.msgprint({
		// 				title: __("Error"),
		// 				indicator: "red",
		// 				message: __("Please select a Middle Man."),
		// 			});
		// 			return;
		// 		}
		// 		if (values.with_proof && !values.proof) {
		// 			frappe.msgprint({
		// 				title: __("Error"),
		// 				indicator: "red",
		// 				message: __("Please attach proof."),
		// 			});
		// 			return;
		// 		}
		// 		frappe.call({
		// 			method: "academia.transactions.doctype.outbox_memo.outbox_memo.create_transaction_document_log",
		// 			args: {
		// 				start_employee: values.start_employee,
		// 				end_employee: frm.doc.recipients[0].recipient,
		// 				document_type: "Outbox Memo",
		// 				document_name: values.document_name,
		// 				document_action_type: "Outbox Memo Action",
		// 				document_action_name: frm.doc.name,
		// 				middle_man: values.middle_man,
		// 				through_middle_man: values.through_middle_man
		// 					? "True"
		// 					: "False",
		// 				proof: values.proof,
		// 				with_proof: values.with_proof ? "True" : "False",
		// 			},
		// 			callback: function (r) {
		// 				if (r.message) {
		// 					console.log(
		// 						"Transaction Document Log created:",
		// 						r.message
		// 					);
		// 					if (r.message) {
		// 						if (
		// 							values.with_proof &&
		// 							!values.through_middle_man
		// 						) {
		// 							frappe.call({
		// 								method: "academia.transactions.doctype.transaction_document_log.transaction_document_log.change_is_received",
		// 								args: {
		// 									doctype: "Outbox Memo",
		// 									docname: frm.doc.outbox_memo,
		// 									is_received: 1,
		// 								},
		// 							})
		// 						} else {
		// 							frappe.call({
		// 								method: "academia.transactions.doctype.transaction_document_log.transaction_document_log.change_is_received",
		// 								args: {
		// 									doctype: "Outbox Memo",
		// 									docname: frm.doc.outbox_memo,
		// 									is_received: 0,
		// 								},
		// 							})
		// 						}
		// 						// location.reload();
		// 					}
		// 				}
		// 			},
		// 			error: function (r) {
		// 				frappe.msgprint("You are in the error")
		// 				console.error(r);
		// 				frappe.msgprint({
		// 					title: __("Error"),
		// 					indicator: "red",
		// 					message: r.message,
		// 				});
		// 			},
		// 		});
		// 	},
		// 	__("Enter Approval Details"),
		// 	__("Submit")
		// );
	},

	on_submit: function (frm) {
		// const new_row_html = generate_new_row_html(
		// 	frm.doc.name,
		// 	frm.doc.type,
		// 	frm.doc.action_date
		// );
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
					if (frm.doc.allow_recipient_to_redirect) {
						frappe.call({
							method: "academia.transactions.doctype.outbox_memo_action.outbox_memo_action.update_outbox_memo",
							args: {
								outbox_memo_name: frm.doc.outbox_memo, // Replace with the current document name
								current_action_maker:
									outbox_memo_action_doc.recipients[0].recipient_email,
								allow_to_redirect: 1, // Uncheck the checkbox
							},
							callback: function (response) {
								if (!response.exc) {
									// frappe.set_route("Form", "Outbox Memo", frm.doc.outbox_memo)
									frappe.set_route("Form", "Outbox Memo", frm.doc.outbox_memo);
									location.reload();
								} else {
									frappe.msgprint("There was an error!");
								}
							},
						});
					} else {
						frappe.call({
							method: "academia.transactions.doctype.outbox_memo_action.outbox_memo_action.update_outbox_memo",
							args: {
								outbox_memo_name: frm.doc.outbox_memo, // Replace with the current document name
								current_action_maker: "", // Set the desired value
								allow_to_redirect: 0, // Uncheck the checkbox
								status: "Completed", // Set status to "Complete"
							},
							callback: function (response) {
								if (!response.exc) {
									frappe.set_route("Form", "Outbox Memo", frm.doc.outbox_memo);
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

		// frappe.call({
		// 	method: "frappe.client.get_value",
		// 	args: {
		// 		doctype: "Outbox Memo",
		// 		fieldname: "related_actions",
		// 		filters: { name: frm.doc.outbox_memo },
		// 	},
		// 	callback: function (response) {
		// 		let current_html = response.message.related_actions || "";
		// 		if (current_html.includes("<table")) {
		// 			// Append the new row to the existing table
		// 			current_html = current_html.replace(
		// 				"</tbody></table>",
		// 				new_row_html + "</tbody></table>"
		// 			);
		// 		} else {
		// 			// Create a new table with the new row
		// 			current_html =
		// 				generate_table_header_html() + new_row_html + "</tbody></table>";
		// 		}

		// 		// Update the related_actions field with the new HTML content
		// 		frappe.call({
		// 			method: "frappe.client.set_value",
		// 			args: {
		// 				doctype: "Outbox Memo",
		// 				name: frm.doc.outbox_memo,
		// 				fieldname: "related_actions",
		// 				value: current_html,
		// 			},
		// 			callback: function (response) {
		// 				if (!response.exc) {
		// 					frappe.msgprint("Related actions updated successfully.");
		// 				} else {
		// 					frappe.msgprint("There was an error updating the related actions.");
		// 				}
		// 			},
		// 		});
		// 	},
		// });
	},

	refresh(frm) {
		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "Outbox Memo",
				name: frm.doc.outbox_memo,
			},
			callback: function (response) {
				if (response.message) {
					const outbox_memo_doc = response.message;

					// Check if the full_electronic field is checked
					if (!outbox_memo_doc.full_electronic) {
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
		// Hide 'add row' button
		frm.get_field("recipients").grid.cannot_add_rows = true;
		// Stop 'add below' & 'add above' options
		frm.get_field("recipients").grid.only_sortable();
		frm.refresh_fields("recipients");
		if (
			frappe.session.user !== "Administrator" &&
			frm.doc.docstatus == 0 &&
			!frm.doc.action_maker
		) {
			frappe.msgprint(frm.doc.docstatus);
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Employee",
					filters: { user_id: frappe.session.user },
				},
				callback: function (response) {
					const employee = response.message;
					if (employee && frm.doc.docstatus == 0) {
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

	before_save: function (frm) {
		// If the user is not an Administrator, set the created_by field to the current user
		frm.set_value("naming_series", frm.doc.outbox_memo + "-ACT-");

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

	onload: function (frm) {
		const outbox_memo = localStorage.getItem("outbox_memo");

		// Set the transaction_reference field value if it exists
		if (outbox_memo && frm.is_new()) {
			frm.set_value("outbox_memo", outbox_memo);
		}
		if (frm.doc.docstatus == 0) {
			frm.set_value("action_date", frappe.datetime.now_date());
		}
		frm.get_field("recipients").grid.cannot_add_rows = true;
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
						method: "academia.transactions.doctype.outbox_memo.outbox_memo.get_direct_reports_to_hierarchy_reverse",
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

function generate_new_row_html(action_name, action_type, action_date) {
	return `<tr><td>${action_name}</td><td>${action_type}</td><td>${action_date}</td></tr>`;
}

function generate_table_header_html() {
	return "<table class='table table-bordered'><thead><tr><th>Action Name</th><th>Action Type</th><th>Action Date</th></tr></thead><tbody>";
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
				default: frm.doc.outbox_memo,
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
					document_type: "Outbox Memo",
					document_name: values.document_name,
					document_action_type: "Outbox Memo Action",
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
										doctype: "Outbox Memo",
										docname: frm.doc.outbox_memo,
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
										doctype: "Outbox Memo",
										docname: frm.doc.outbox_memo,
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
