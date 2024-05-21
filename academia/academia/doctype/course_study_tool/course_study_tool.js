// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on('Course Study Tool', {
    "get_courses": function(frm) {
		frm.set_value("courses",[]);
		frappe.call({
			method: "get_courses",
			doc:frm.doc,
			callback: function(r) {
				if(r.message) {
					frm.set_value("courses", r.message);
				}
			}
		});
	},
	"generate_courses": function(frm) {
		//frm.set_value("courses",[]);
		frappe.call({
			method: "generate_courses",
			doc:frm.doc,
			callback: function(r) {
				if(r.message) {
					//frm.set_value("courses", r.message);
				}
			}
		});
	}
});
