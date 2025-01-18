// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Transaction New", {
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
		if (frm.doc.status === "Pending" && frm.doc.docstatus != 0) {
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
											"You can't create a new document while another document is still pending."
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
				"Add Document"
			);
			if(frappe.user_roles.includes("Inbox Memo Maker")){
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
												"You can't create a new document while another document is still pending."
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
					"Add Document"
				);
			}
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
											"You can't create a new document while another document is still pending."
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
				"Add Document"
			);
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
											"You can't create a new document while another document is still pending."
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
				"Add Document"
			);
		}
	},
});
