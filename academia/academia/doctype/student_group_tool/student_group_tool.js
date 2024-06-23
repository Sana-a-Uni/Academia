// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Group Tool', {
    "get_students": function(frm) {
        frm.set_value("students",[]);
		frappe.call({
			method: "get_students",
			doc:frm.doc,
			callback: function(r) {
				if(r.message) {
					frm.set_value("students", r.message);
				}
			}
		});
	},
	"generate_groups": function(frm) {
		//frm.set_value("courses",[]);
		frappe.call({
			method: "generate_groups",
			doc:frm.doc,
			callback: function(r) {
				if(r.message) {
					//frm.set_value("courses", r.message);
				}
			}
		});
	}
});
