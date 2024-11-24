// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Program Enrollment Tool", {
	refresh: function (frm) {
		// زر Import Data
		frm.add_custom_button(
			__("Import Data"),
			function () {
				// إعداد الرابط لشاشة Data Import
				const url = frappe.urllib.get_full_url(
					"/app/data-import/new?reference_doctype=Temporary Student&import_type=Insert New Records"
				);

				// فتح الرابط في نافذة جديدة
				window.open(url, "_blank");
			},
			__("Actions")
		);
	},
});
