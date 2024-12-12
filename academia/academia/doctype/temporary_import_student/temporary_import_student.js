// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Temporary Import Student", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Temporary Import Student", {
	refresh: function (frm) {
		// زر Import Data
		frm.add_custom_button(
			__("Import New Records"),
			function () {
				// إعداد الرابط لشاشة Data Import
				const url = frappe.urllib.get_full_url(
					"/app/data-import/new?reference_doctype=Temporary Import Student&import_type=Insert New Records"
				);

				// فتح الرابط في نافذة جديدة
				window.open(url, "_blank");
			},
			__("Import Data")
		);

		frappe.listview_settings["Temporary Import Student"] = {
			refresh: function (listview) {
				listview.page.add_menu_item(__("My Page Button"), function () {
					frappe.msgprint(__("Page button clicked!"));
				});
			},
		};
	},
});
