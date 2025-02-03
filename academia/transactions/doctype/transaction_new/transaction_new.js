// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

let delegated_employees_emails = [];

frappe.ui.form.on("Transaction New", {
	before_submit: function (frm) {
		frm.set_value("transaction_holder", frappe.session.user);
		frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "Employee",
                filters: { user_id: frappe.session.user },
                fieldname: "company"
            },
            callback: function(response) {
                if (response.message) {
                    let company = response.message.company;
                    // Set the company field with the fetched company
                    frm.set_value("company", company);
                }
            }
        });
	},
	refresh(frm) {
		localStorage.setItem("transaction_reference", frm.doc.name);

		frm.get_field("related_documents").grid.cannot_add_rows = true;
		// Stop 'add below' & 'add above' options
		frm.get_field("related_documents").grid.only_sortable();
		frm.refresh_fields("related_documents");
		frm.doc.related_documents.forEach(function (row, index) {
			// Fetch the status of each document
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: row.document_type,
					fieldname: "status",
					filters: { name: row.document_name },
				},
				callback: function (response) {
					if (response.message) {
						const status = response.message.status;
						// Update the status in the child table
						frm.doc.related_documents[index].status = status;
						frm.refresh_field("related_documents");
					} else {
						frappe.msgprint(
							`Unable to fetch status for document: ${row.document_name}`
						);
					}
				},
			});
		});
		if(frm.doc.transaction_holder == frappe.session.user && frm.doc.status === "Pending" && frm.doc.docstatus != 0){
			if (frm.doc.related_documents.length > 0) {
				frappe.call({
					method: "frappe.client.get_value",
					args: {
						doctype:
							frm.doc.related_documents[frm.doc.related_documents.length - 1]
								.document_type,
						fieldname: "status",
						filters: {
							name: frm.doc.related_documents[
								frm.doc.related_documents.length - 1
							].document_name,
						},
					},
					callback: function (response) {
						if (response.message) {
							add_buttons(frm);
						} else {
							frappe.msgprint("Unable to fetch status for document: " + frm.doc.related_documents[frm.doc.related_documents.length - 1].document_name);
						}
					},
				});
			} else {
				add_buttons(frm);
			}
			// if (frm.doc.status === "Pending" && frm.doc.docstatus != 0
			// 	&& frm.doc.related_documents.length == 0 || ((frm.doc.related_documents.length > 0 && frm.doc.related_documents[0].status != "Pending"))
			// ) {
			// 	add_transfer_transaction_button(frm);
			// 	add_create_sub_transaction_button(frm)
			// 	add_request_button(frm);
			// 	add_outbox_memo_button(frm);
			// 	add_specific_transaction_document_button(frm);
			// 	add_review_elegated_employees_emails.includes(frappe.session.user)transaction_button(frm);
			// 	if(frappe.user_roles.includes("Inbox Memo Maker")){
			// 		add_inbox_memo_button(frm);
			// 	}
			// }
		}
		else if (frm.doc.transaction_holder != frappe.session.user && frm.doc.status === "Pending" && frm.doc.docstatus != 0 ) {
			frappe.call({
				method: "frappe.client.get_list",
				args: {
					doctype: "Employee Proxy",
					filters: { "employee_email": frm.doc.transaction_holder },
					fields: ["name"]  // Just fetch the name to check existence
				},
				callback: function(response) {
					if (response.message && response.message.length > 0) {
						// Employee Proxy exists, now proceed with getting details
						frappe.call({
							method: "frappe.client.get",
							args: {
								doctype: "Employee Proxy",
								filters: { "employee_email": frm.doc.transaction_holder }
							},
							callback: function(response) {
								if (response.message) {
									let delegated_employees = response.message.delegated_employees;
									let delegated_employees_emails = delegated_employees.map(emp => emp.email);
			
									// Check if current user is one of the delegated employees
									if (delegated_employees_emails.includes(frappe.session.user)) {
										// User is a delegated employee, so proceed with the button logic
										if (frm.doc.related_documents.length > 0) {
											frappe.call({
												method: "frappe.client.get_value",
												args: {
													doctype: frm.doc.related_documents[frm.doc.related_documents.length - 1].document_type,
													fieldname: "status",
													filters: {
														name: frm.doc.related_documents[frm.doc.related_documents.length - 1].document_name,
													},
												},
												callback: function(response) {
													if (response.message) {
														if (response.message.status != "Pending") {
															add_buttons(frm);
														}
													} else {
														frappe.msgprint("Unable to fetch status for document: " + frm.doc.related_documents[frm.doc.related_documents.length - 1].document_name);
													}
												}
											});
										} else {
											add_buttons(frm);
										}
			
										// If status is pending and user is a delegated employee, add buttons
										if (frm.doc.status === "Pending" && frm.doc.docstatus != 0 &&
											(frm.doc.related_documents.length == 0 || 
											(frm.doc.related_documents.length > 0 && frm.doc.related_documents[frm.doc.related_documents.length - 1].status != "Pending"))
										) {
											add_buttons(frm);
										}
									}
								} else {
									console.log("No delegated employees found for the transaction holder.");
								}
							}
						});
					} else {
						console.log("No Employee Proxy found for the given employee email.");
					}
				}
			});
		}
		

		
	},
});
function add_buttons(frm) {
    add_transfer_transaction_button(frm);
    add_create_sub_transaction_button(frm);
    add_request_button(frm);
    add_outbox_memo_button(frm);
    add_specific_transaction_document_button(frm);
    add_review_transaction_button(frm);
    if (frappe.user_roles.includes("Inbox Memo Maker")) {
        add_inbox_memo_button(frm);
    }
}
function add_transfer_transaction_button(frm){
	frm.add_custom_button(__('Transfer Transaction'), function() {
		frappe.prompt([
			{
				label: 'New Holder',
				fieldname: 'new_holder',
				fieldtype: 'Link',
				options: 'Employee',
				reqd: 1,
				get_query: function() {
					return {
						filters: {
							company: frm.doc.company,
							user_id: ["not in", [frappe.session.user, frm.doc.transaction_holder]]
						}
					};
				}
			}
		], function(values) {
			// Fetch the user_id of the selected employee
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Employee",
					filters: { name: values.new_holder },
					fieldname: "user_id"
				},
				callback: function(response) {
					if (response.message) {
						let user_id = response.message.user_id;
						// Update the transaction_holder field with the user_id of the selected employee
						frm.set_value('transaction_holder', user_id)
						.then(() => {frm.save_or_update(); });
						
					}
				}
			});
		}, __('Transfer Transaction'), __('Transfer'));
	});
}

function add_create_sub_transaction_button(frm){
	frm.add_custom_button(__('Create Sub-Transaction'), function() {
		frappe.prompt([
			{
				label: 'Title',
				fieldname: 'title',
				fieldtype: 'Data',
				reqd: 1
			},
		], function(values) {
			// Create a new sub-transaction document
			frappe.call({
				method: "frappe.client.insert",
				args: {
					doc: {
						doctype: "Transaction New",
						title: values.title,
						parent_transaction: frm.doc.name,
						is_sub_transaction: 1,
						transaction_holder: frappe.session.user,
					}
				},
				callback: function(response) {
					if (response.message) {
						let new_sub_transaction = response.message;
						// Submit the new sub-transaction document
						frappe.call({
							method: "frappe.client.submit",
							args: {
								doc: new_sub_transaction
							},
							callback: function(submit_response) {
								if (submit_response.message) {
									// Add the new sub-transaction to the sub_transactions child table
									let new_row = frm.add_child('sub_transactions');
									new_row.transaction = new_sub_transaction.name;
									new_row.title = new_sub_transaction.title;
									new_row.status = new_sub_transaction.status;
									frm.refresh_field('sub_transactions');
									frm.save_or_update();
								}
							}
						});
					}
				}
			});
		}, __('Create Sub-Transaction'), __('Create'));
	});
}

function add_request_button(frm){
	frm.add_custom_button(
		__("Request"),
		function () {
			if (frm.doc.related_documents.length > 0) {
				frappe.call({
					method: "frappe.client.get_value",
					args: {
						doctype:
							frm.doc.related_documents[frm.doc.related_documents.length - 1]
								.document_type,
						fieldname: "status",
						filters: {
							name: frm.doc.related_documents[
								frm.doc.related_documents.length - 1
							].document_name,
						},
					},
					callback: function (response) {
						if (response.message) {
							if (response.message.status == "Pending") {
								frappe.throw(
									__("You can't create a new document while another document is still pending.")
								);
							} else {
								const url = frappe.urllib.get_full_url(
									"/app/request/new?transaction_reference=" +
										frm.doc.name
								);

								window.location.href = url;
							}
						} else {
							const url = frappe.urllib.get_full_url(
								"/app/request/new?transaction_reference=" + frm.doc.name
							);

							window.location.href = url;
						}
					},
				});
			} else {
				const url = frappe.urllib.get_full_url(
					"/app/request/new?transaction_reference=" + frm.doc.name
				);

				window.location.href = url;
			}
		},
		__("Add Document")
	);
}

function add_inbox_memo_button(frm){
	frm.add_custom_button(
		__("Inbox Memo"),
		function () {
			if (frm.doc.related_documents.length > 0) {
				frappe.call({
					method: "frappe.client.get_value",
					args: {
						doctype:
							frm.doc.related_documents[frm.doc.related_documents.length - 1]
								.document_type,
						fieldname: "status",
						filters: {
							name: frm.doc.related_documents[
								frm.doc.related_documents.length - 1
							].document_name,
						},
					},
					callback: function (response) {
						if (response.message) {
							if (response.message.status == "Pending") {
								frappe.throw(
									__("You can't create a new document while another document is still pending.")
								);
							} else {
								const url = frappe.urllib.get_full_url(
									"/app/inbox-memo/new?transaction_reference=" +
										frm.doc.name
								);

								window.location.href = url;
							}
						} else {
							const url = frappe.urllib.get_full_url(
								"/app/inbox-memo/new?transaction_reference=" + frm.doc.name
							);

							window.location.href = url;
						}
					},
				});
			} else {
				const url = frappe.urllib.get_full_url(
					"/app/inbox-memo/new?transaction_reference=" + frm.doc.name
				);

				window.location.href = url;
			}
		},
		__("Add Document")
	);
}

function add_outbox_memo_button(frm){
	frm.add_custom_button(
		__("Outbox Memo"),
		function () {
			if (frm.doc.related_documents.length > 0) {
				frappe.call({
					method: "frappe.client.get_value",
					args: {
						doctype:
							frm.doc.related_documents[frm.doc.related_documents.length - 1]
								.document_type,
						fieldname: "status",
						filters: {
							name: frm.doc.related_documents[
								frm.doc.related_documents.length - 1
							].document_name,
						},
					},
					callback: function (response) {
						if (response.message) {
							if (response.message.status == "Pending") {
								frappe.throw(
									__("You can't create a new document while another document is still pending.")
								);
							} else {
								const url = frappe.urllib.get_full_url(
									"/app/outbox-memo/new?transaction_reference=" +
										frm.doc.name
								);

								window.location.href = url;
							}
						} else {
							const url = frappe.urllib.get_full_url(
								"/app/outbox-memo/new?transaction_reference=" +
									frm.doc.name
							);

							window.location.href = url;
						}
					},
				});
			} else {
				const url = frappe.urllib.get_full_url(
					"/app/outbox-memo/new?transaction_reference=" + frm.doc.name
				);

				window.location.href = url;
			}
		},
		__("Add Document")
	);
}

function add_specific_transaction_document_button(frm){
	frm.add_custom_button(
		__("Specific Transaction Document"),
		function () {
			if (frm.doc.related_documents.length > 0) {
				frappe.call({
					method: "frappe.client.get_value",
					args: {
						doctype:
							frm.doc.related_documents[frm.doc.related_documents.length - 1]
								.document_type,
						fieldname: "status",
						filters: {
							name: frm.doc.related_documents[
								frm.doc.related_documents.length - 1
							].document_name,
						},
					},
					callback: function (response) {
						if (response.message) {
							if (response.message.status == "Pending") {
								frappe.throw(
									__("You can't create a new document while another document is still pending.")
								);
							} else {
								const url = frappe.urllib.get_full_url(
									"/app/specific-transaction-document/new?transaction_reference=" +
										frm.doc.name
								);

								window.location.href = url;
							}
						} else {
							const url = frappe.urllib.get_full_url(
								"/app/specific-transaction-document/new?transaction_reference=" +
									frm.doc.name
							);

							window.location.href = url;
						}
					},
				});
			} else {
				const url = frappe.urllib.get_full_url(
					"/app/specific-transaction-document/new?transaction_reference=" +
						frm.doc.name
				);

				window.location.href = url;
			}
		},
		__("Add Document")
	);
}

function add_review_transaction_button(frm){
	frm.add_custom_button(
		__("Review Transactions"),
		function () {
			if (frm.doc.related_documents.length > 0) {
				frappe.call({
					method: "frappe.client.get_value",
					args: {
						doctype:
							frm.doc.related_documents[frm.doc.related_documents.length - 1]
								.document_type,
						fieldname: "status",
						filters: {
							name: frm.doc.related_documents[
								frm.doc.related_documents.length - 1
							].document_name,
						},
					},
					callback: function (response) {
						if (response.message) {
							if (response.message.status == "Pending") {
								frappe.throw(
									__("You can't create a new document while another document is still pending.")
								);
							} else {
								const url = frappe.urllib.get_full_url(
									"/app/review-transactions/new?transaction_reference=" +
										frm.doc.name
								);

								window.location.href = url;
							}
						} else {
							const url = frappe.urllib.get_full_url(
								"/app/review-transactions/new?transaction_reference=" +
									frm.doc.name
							);

							window.location.href = url;
						}
					},
				});
			} else {
				const url = frappe.urllib.get_full_url(
					"/app/review-transactions/new?transaction_reference=" +
						frm.doc.name
				);

				window.location.href = url;
			}
		},
		__("Add Document")
	);
}