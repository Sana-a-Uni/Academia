// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt
let mustInclude = [];
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
					method: "academia.transactions.doctype.request.request.create_new_request_action",
					args: {
						user_id: frappe.session.user,
						request: frm.doc.name,
						type: "Approved",
						details: values.details || "",
						// request: frm.doc.request || "",
					},
					callback: function (r) {
						if (r.message) {
							// console.log(r.message);
							if (r.message) {
								location.reload();
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
				if (!values.details) {
					frappe.msgprint({
						title: __("Error"),
						indicator: "red",
						message: __("Please enter rejection details."),
					});
					return;
				}
				frappe.call({
					method: "academia.transactions.doctype.request.request.create_new_request_action",
					args: {
						user_id: frappe.session.user,
						request: frm.doc.name,
						type: "Rejected",
						details: values.details || "",
						// request: frm.doc.request || "",
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
	localStorage.setItem("request", frm.doc.name);

	cur_frm.page.add_action_item(__("Redirect"), function () {
		const url = frappe.urllib.get_full_url(
			"/app/request-action/new?request=" + frm.doc.name + "&type=Redirected"
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

frappe.ui.form.on("Request", {
	on_submit: function (frm) {
		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "Transaction New",
				filters: {
					name: frm.doc.transaction_reference,
				},
			},
			callback: function (response) {
				if (response.message) {
					let transaction_new_doc = response.message;
					transaction_new_doc.related_documents.push({
						document_name: frm.doc.name,
						document_type: frm.doc.doctype,
						document_title: frm.doc.title,
						document_status: frm.doc.status,
					});
					frappe.call({
						method: "frappe.client.save",
						args: {
							doc: transaction_new_doc,
						},
						callback: function (save_response) {
							if (save_response.message) {
								frappe.set_route(
									"Form",
									"Transaction New",
									frm.doc.transaction_reference
								);
							}
						},
					});
				}
			},
		});
	},
	before_submit: function (frm) {
		current_action_maker = frm.doc.using_path_template ?frm.doc.recipients_path[0].recipient_email : frm.doc.recipients[0].recipient_email;
		frm.set_value("current_action_maker", current_action_maker);
		frappe.db
			.set_value(
				"Transaction New",
				frm.doc.transaction_reference,
				"transaction_holder",
				current_action_maker
			)
			.then(() => {
				frappe.call({
					method: "academia.transactions.doctype.request.request.update_share_permissions",
					args: {
						docname: frm.doc.name,
						user: frappe.session.user,
						permissions: {
							read: 1,
							write: 1,
							share: 1,
							submit: 1,
						},
					},
					callback: function (response) {
						if (response.message) {
							// frappe.db.set_value(inbox_memo , 'current_action_maker')
							frappe.db.set_value(
								"Request",
								frm.doc.name,
								"current_action_maker",
								current_action_maker
							)
							.then(() => {
								frappe.db
									.set_value(
										"Transaction New",
										frm.doc.transaction_reference,
										"transaction_holder",
										current_action_maker
									)
									.then(() => {
										location.reload();
									});
							});
							// back to Transaction after save the transaction action
							
						}
					},
				});
			});
		
	},

	refresh(frm) {
		if (
			frm.doc.current_action_maker == frappe.session.user &&
			(frm.doc.is_received || frm.doc.full_electronic)
		) {
			add_approve_action(frm);
			add_reject_action(frm);
			add_redirect_action(frm);
		} else if (
			frm.doc.current_action_maker != frappe.session.user && frm.doc.docstatus == 1 &&
			(frm.doc.is_received || frm.doc.full_electronic)
		) {
			frappe.call({
				method: "frappe.client.get_list",
				args: {
					doctype: "Employee Proxy",
					filters: { employee_email: frm.doc.current_action_maker },
					fields: ["name"] // Fetching just the name to check existence
				},
				callback: function(response) {
					if (response.message && response.message.length > 0) {
						// Employee Proxy exists, now proceed with getting details
						frappe.call({
							method: "frappe.client.get",
							args: {
								doctype: "Employee Proxy",
								filters: { employee_email: frm.doc.current_action_maker }
							},
							callback: function(response) {
								if (response.message) {
									let delegated_employees = response.message.delegated_employees;
									let delegated_employees_emails = delegated_employees.map(emp => emp.email);
									console.log("Delegated Employees Emails:", delegated_employees_emails);
			
									if (delegated_employees_emails.includes(frappe.session.user)) {
										add_approve_action(frm);
										add_reject_action(frm);
										add_redirect_action(frm);
									}
								}
							}
						});
					} else {
						console.log("No Employee Proxy found for the given employee email.");
					}
				}
			});
			
		}
		// Hide 'add row' button
		frm.get_field("recipients").grid.cannot_add_rows = true;
		// Stop 'add below' & 'add above' options
		frm.get_field("recipients").grid.only_sortable();
		frm.refresh_fields("recipients");

		if (frm.doc.docstatus != 0) {
			frm.fields_dict.get_recipients.$wrapper.hide();
			frm.fields_dict.get_recipients.input.disabled = true;
			frm.fields_dict.clear_recipients.$wrapper.hide();
			frm.fields_dict.clear_recipients.input.disabled = true;
		}
	},

	onload: function (frm) {
		document.addEventListener("keydown", function (event) {
			// Check if the Ctrl + B combination is pressed
			if (event.ctrlKey && event.key === "b") {
				// Check if the current doctype is one of the specified doctypes
				if (frm.doctype === "Request") {
					// Prevent the default action and stop propagation
					event.preventDefault();
					event.stopPropagation();
					frappe.msgprint(__("The shortcut Ctrl + B is disabled for this doctype."));
				}
			}
		});
		const transaction_reference = localStorage.getItem("transaction_reference");

		// Set the transaction_reference field value if it exists
		if (transaction_reference && frm.is_new()) {
			frm.set_value("transaction_reference", transaction_reference);
		}
		if (!frm.doc.start_from) {
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Employee",
					filters: { user_id: frappe.session.user },
					fieldname: "name",
				},
				callback: function (response) {
					if (response.message && frm.is_new()) {
						frm.set_value("start_from", response.message.name);
					}
				},
			});
		}
	},

	start_from: function(frm){
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
					company: frm.doc.start_from_company,
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

	template_name: function(frm) {
		if(!frm.doc.template_name)
		{
			// Clear if template_name is empty
            frm.doc.recipients_path = [];
            frm.refresh_field('recipients_path'); 
		}
		else
		{
			frappe.call({
				method: 'academia.transactions.doctype.request.request.copy_template_paths',
				args: {
					template_docname: frm.doc.template_name
				},
				callback: function(r) {
					if (r.message) {
						// Clear existing entries in the recipients_path child table
						frm.clear_table('recipients_path');
		
						// Add new entries
						r.message.forEach(function(item) {
							let child = frm.add_child('recipients_path');
							frappe.model.set_value(child.doctype, child.name, 'step', item.step);
							frappe.model.set_value(child.doctype, child.name, 'recipient_company', item.recipient_company);
							frappe.model.set_value(child.doctype, child.name, 'recipient_department', item.recipient_department);
							frappe.model.set_value(child.doctype, child.name, 'recipient_designation', item.recipient_designation);
						});
		
						frm.refresh_field('recipients_path');
					}
				}
			});
		}
    },

});

function update_must_include(frm) {
	if (frm.doc.start_from) {
		frm.clear_table("recipients");
		frm.refresh_field("recipients");

		frappe.call({
			method: "academia.transactions.doctype.request.request.get_reports_to_hierarchy",
			args: {
				employee_name: frm.doc.start_from,
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

frappe.ui.form.on("Request", {
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
		method: "academia.transactions.doctype.request.request.get_request_actions_html",
		args: {
			request_name: frm.doc.name,
		},
		callback: function (r) {
			if (r.message) {
				frm.set_df_property("related_actions", "options", r.message);
				frm.refresh_field("related_actions");
			}
		},
	});
}
