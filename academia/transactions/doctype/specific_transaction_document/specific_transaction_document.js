// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

let mustInclude = [];
let global_current_employee = null;
let global_next_recipient = null;
let global_action_name = null;

frappe.ui.form.on("Specific Transaction Document", {
	onload: function (frm) {
		frm.get_field("recipients").grid.cannot_add_rows = true;
	},
	before_submit: function (frm) {
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
	},
	refresh(frm) {
		// Assign global variables
		frappe.call({
			method: "frappe.client.get_value",
			args: {
				doctype: "Employee",
				filters: { user_id: frappe.session.user },
				fieldname: ["name", "reports_to"],
			},
			callback: function (response) {
				if (response.message) {
					global_current_employee = response.message.name;
					if (
						frm.doc.direction == "Upward" &&
						global_current_employee != frm.doc.recipients[0].recipient
					) {
						global_next_recipient = response.message.reports_to;
					}
				}
			},
		});

		if (frm.doc.current_action_maker === frappe.session.user) {
			add_approve_action(frm);
			if (frm.doc.allow_to_redirect === 1) {
				add_redirect_action(frm);
			}
			add_reject_action(frm);
			// add_reject_action(frm);
		}
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
});
function update_must_include(frm) {
	if (frm.doc.start_from) {
		frm.clear_table("recipients");
		frm.refresh_field("recipients");

		frappe.call({
			method: "academia.transactions.doctype.specific_transaction_document.specific_transaction_document.get_reports_to_hierarchy",
			args: {
				employee_name: frm.doc.start_from,
			},
			callback: function (response) {
				mustInclude = response.message;
			},
		});
	}
}
function add_approve_action(frm) {
	cur_frm.page.add_action_item(__("Approve"), function () {
		if (
			(frm.doc.direction == "Upward" &&
				global_current_employee === frm.doc.recipients[0].recipient) ||
			frm.doc.full_electronic ||
			frm.doc.direction == "Downward"
		) {
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
						method: "academia.transactions.doctype.specific_transaction_document.specific_transaction_document.create_new_specific_transaction_document_action",
						args: {
							user_id: frappe.session.user,
							specific_transaction_document: frm.doc.name,
							type: "Approved",
							details: values.details || "",
						},
						callback: function (r) {
							if (r.message) {
								// console.log(r.message);
								if (r.message) {
									frappe.db
										.set_value(
											"Specific Transaction Document",
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
		} else {
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
						default: frm.doc.name,
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
						default: global_current_employee || "",
					},
					{
						fieldname: "end_employee",
						fieldtype: "Link",
						label: "End To",
						options: "Employee",
						default: global_next_recipient || "",
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
						method: "academia.transactions.doctype.specific_transaction_document.specific_transaction_document.create_new_specific_transaction_document_action",
						args: {
							user_id: frappe.session.user,
							specific_transaction_document: frm.doc.name,
							type: "Approved",
							details: values.details || "",
						},
						callback: function (r) {
							if (r.message) {
								// console.log(r.message);
								if (r.message) {
									frappe.db
										.set_value(
											"Specific Transaction Document",
											frm.docname,
											"current_action_maker",
											r.message.action_maker
										)
										.then(() => {
											console.log(r.message);
											global_action_name = r.message.action_name;
											console.log(global_action_name);

											frappe.call({
												method: "academia.transactions.doctype.outbox_memo.outbox_memo.create_transaction_document_log",
												args: {
													start_employee: values.start_employee,
													end_employee: global_next_recipient,
													document_type: "Specific Transaction Document",
													document_name: values.document_name,
													document_action_type:
														"Specific Transaction Document Action",
													document_action_name: global_action_name,
													middle_man: values.middle_man,
													through_middle_man: values.through_middle_man
														? "True"
														: "False",
													proof: values.proof,
													with_proof: values.with_proof
														? "True"
														: "False",
												},
												callback: function (r) {
													if (r.message) {
														console.log(
															"Transaction Document Log created:",
															r.message
														);
														if (r.message) {
															if (
																values.with_proof &&
																!values.through_middle_man
															) {
																frappe.db
																	.set_value(
																		"Specific Transaction Document",
																		frm.docname,
																		"is_received",
																		1
																	)
																	.then(() => {
																		location.reload();
																	});
															} else {
																frappe.db
																	.set_value(
																		"Specific Transaction Document",
																		frm.docname,
																		"is_received",
																		0
																	)
																	.then(() => {
																		location.reload();
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
										});
								}

								// Fetch the next recipient based on the next step
								// frappe.call({
								// 	method: "academia.transaction_management.doctype.transaction.transaction.get_next_recipient_by_step",
								// 	args: {
								// 		transaction_name: values.transaction_name,
								// 		current_employee: start_employee,
								// 	},
								// 	callback: function (r) {
								// 		if (r.message) {
								// 			const end_employee = r.message;
								// 			console.log(end_employee)
								// 			// Call the server-side method to create the transaction paper log

								// 		} else {
								// 			frappe.msgprint(__("No next recipient found."));
								// 		}
								// 	},
								// 	error: function (r) {
								// 		console.error(r);
								// 	},
								// });
								// if (r.message) {
								// 	location.reload();
								// }
								// frappe.db.set_value('Transaction', frm.docname, 'status', 'Approved');
							}
						},
					});
				},
				__("Enter Approval Details"),
				__("Submit")
			);
		}
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
					method: "academia.transactions.doctype.specific_transaction_document.specific_transaction_document.create_new_specific_transaction_document_action",
					args: {
						user_id: frappe.session.user,
						specific_transaction_document: frm.doc.name,
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

function add_redirect_action(frm) {
	cur_frm.page.add_action_item(__("Redirect"), function () {
		const url = frappe.urllib.get_full_url(
			"/app/specific-transaction-document-action/new?specific_transaction_document=" +
				frm.doc.name +
				"&type=Redirected"
		);

		// فتح الرابط في نافذة جديدة
		window.location.href = url;
		// frappe.new_doc("Inbox Memo Action", {
		// 	inbox_memo: frm.doc.name,
		// 	type: "Redirected",
		// 	from_company: frm.doc.start_from_company,
		// 	from_department: frm.doc.start_from_department,
		// 	from_designation: frm.doc.start_from_designation,
		// 	// received: is_received,
		// });
		// // back to Transaction after save the transaction action
		// frappe.ui.form.on("Inbox Memo Action", {
		// 	on_submit: function () {
		// 		if (frm.doc.inbox_memo) { frappe.msgprint(frm.doc.inbox_memo) }
		// 		else { frappe.msgprint("")}
		// 		frappe.call({
		// 			method: "academia.transactions.doctype.inbox_memo.inbox_memo.update_share_permissions",
		// 			args: {
		// 				docname: frm.doc.name,
		// 				user: frappe.session.user,
		// 				permissions: {
		// 					read: 1,
		// 					write: 0,
		// 					share: 0,
		// 					submit: 0,
		// 				},
		// 			},
		// 			callback: function (response) {
		// 				if (response.message) {
		// 					inbox_memo_action_doc = frappe.get_doc("Inbox Memo Action", frm.doc)
		// 					// frappe.db.set_value(inbox_memo , 'current_action_maker')
		// 					frappe.db.set_value("Inbox Memo", frm.doc.inbox_memo, "current_action_maker", inbox_memo_action_doc.recipients[0].recipient_email);
		// 					// back to Transaction after save the transaction action
		// 					frappe.set_route("Form", "Inbox Memo", frm.doc.name);
		// 					location.reload();
		// 				}
		// 			},
		// 		});
		// 	},
		// });
	});
}

frappe.ui.form.on("Specific Transaction Document", {
	refresh: function (frm) {
		update_related_actions_html(frm);
	},
	after_save: function (frm) {
		update_related_actions_html(frm);
	},
	onload: function (frm) {
		update_related_actions_html(frm);
	},
});

function update_related_actions_html(frm) {
	frappe.call({
		method: "academia.transactions.doctype.specific_transaction_document.specific_transaction_document.get_specific_transaction_document_actions_html",
		args: {
			specific_transaction_document_name: frm.doc.name,
		},
		callback: function (r) {
			if (r.message) {
				frm.set_df_property("related_actions", "options", r.message);
				frm.refresh_field("related_actions");
			}
		},
	});
}
