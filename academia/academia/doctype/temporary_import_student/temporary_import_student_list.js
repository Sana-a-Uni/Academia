frappe.listview_settings["Temporary Import Student"] = {
	onload: function (list_view) {
		list_view.page.add_inner_button(__("Enroll Studetns"), function () {
			frappe.call({
				method: "academia.academia.doctype.temporary_import_student.temporary_import_student.enroll_students",
				callback: function (r) {
					if (!r.exc) {
						frappe.msgprint(__("Students have been successfully enrolled."));
						frm.reload_doc();
					}
				},
			});
		});
	},
};
