// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt
let document = null;

frappe.ui.form.on("Transaction Document Log", {
	refresh: function (frm) {
		frm.disable_save();

		// get the origianl document
		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: frm.doc.document_type,
				name: frm.doc.document_name,
			},
			callback: function (response) {
				if (response.message) {
					document = response.message;
				} else {
					callback("Unable to fetch the document.");
				}
			},
		});

		if (frm.doc.paper_progress == __("Delivered to middle man")) {
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Employee",
					fieldname: "user_id",
					filters: { name: frm.doc.middle_man },
				},
				callback: function (r) {
					if (r.message) {
						var middle_man_user_id = r.message.user_id;
						if (frappe.session.user == middle_man_user_id) {
							add_middle_man_received_action(frm);
						}
					}
				},
			});
		} else if (frm.doc.paper_progress == __("Received by middle man")) {
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Employee",
					fieldname: "user_id",
					filters: { name: frm.doc.middle_man },
				},
				callback: function (r) {
					if (r.message) {
						var middle_man_user_id = r.message.user_id;
						if (frappe.session.user == middle_man_user_id) {
							add_middle_man_delivered_action(frm);
						}
					}
				},
			});
		} else if (frm.doc.paper_progress == __("Delivered to end employee")) {
			frappe.call({
				method: "frappe.client.get_value",
				args: {
					doctype: "Employee",
					fieldname: "user_id",
					filters: { name: frm.doc.end_employee },
				},
				callback: function (r) {
					if (r.message) {
						var end_employee_user_id = r.message.user_id;
						if (frappe.session.user == end_employee_user_id) {
							add_end_employee_received_action(frm);
						}
					}
				},
			});
		}
	},
});

function add_middle_man_received_action(frm) {
	cur_frm.page.add_action_item(__("Received"), function () {
		const attachments = frm.doc.attachments || [];
		let attachmentList = attachments
			.map(
				(attachment) =>
					`- ${attachment.attachment_label} (${attachment.number_of_papers} ${__(
						"papers"
					)})`
			)
			.join("<br>");

		let confirmationMessage = `
			<p>${__("Make sure you have received all the documents before accepting:")}</p>
			<p>${attachmentList}</p>
			<p>${__("Are you sure you have all these documents?")}</p>
		`;

		frappe.confirm(confirmationMessage, function () {
			frappe.db
				.set_value(
					"Transaction Document Log",
					frm.docname,
					"paper_progress",
					__("Received by middle man")
				)
				.then(() => {
					location.reload();
				})
				.catch((error) => {
					frappe.msgprint({
						title: __("Error"),
						indicator: "red",
						message: __("An error occurred while updating the document."),
					});
					console.error(error);
				});
		});
	});
}

function add_middle_man_delivered_action(frm) {
	cur_frm.page.add_action_item(__("Delivered"), function () {
		frappe.prompt(
			[
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
				if (values.with_proof == 1 && !values.proof) {
					frappe.msgprint({
						title: __("Error"),
						indicator: "red",
						message: __("Please attach proof."),
					});
					return;
				} else if (values.with_proof == 1 && values.proof) {
					frappe.db.set_value("Transaction Document Log", frm.docname, {
						paper_progress: __("Received by end employee"),
						ee_proof: values.proof,
					});
					frappe.call({
						method: "academia.transactions.doctype.transaction_document_log.transaction_document_log.change_is_received",
						args: {
							doctype: frm.doc.document_type,
							docname: frm.doc.document_name,
							is_received: 1,
						},
						callback: function (response) {
							if (response.message) {
								location.reload();
							}
						},
					});
					location.reload();
				} else {
					frappe.db.set_value(
						"Transaction Document Log",
						frm.docname,
						"paper_progress",
						__("Delivered to end employee")
					);
					location.reload();
				}
			}
		);
	});
}

function add_end_employee_received_action(frm) {
	cur_frm.page.add_action_item(__("Received"), function () {
		const attachments = frm.doc.attachments || [];
		let attachmentList = attachments
			.map(
				(attachment) =>
					`- ${attachment.attachment_label} (${attachment.number_of_papers} ${__(
						"papers"
					)})`
			)
			.join("<br>");

		let confirmationMessage = `
			<p>${__("Make sure you have received all the documents before accepting:")}</p>
			<p>${attachmentList}</p>
			<p>${__("Are you sure you have all these documents?")}</p>
		`;

		frappe.confirm(confirmationMessage, function () {
			frappe.db
				.set_value(
					"Transaction Document Log",
					frm.docname,
					"paper_progress",
					__("Received by end employee")
				)
				.then(() => {
					frappe.call({
						method: "academia.transactions.doctype.transaction_document_log.transaction_document_log.change_is_received",
						args: {
							doctype: frm.doc.document_type,
							docname: frm.doc.document_name,
							is_received: 1,
						},
						callback: function (response) {
							if (response.message) {
								location.reload();
							}
						},
					});
				})
				.catch((error) => {
					frappe.msgprint({
						title: __("Error"),
						indicator: "red",
						message: __("An error occurred while updating the document."),
					});
					console.error(error);
				});
		});
	});
}
