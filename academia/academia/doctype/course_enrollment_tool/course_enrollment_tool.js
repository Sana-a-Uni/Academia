// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on('Course Enrollment Tool', {
    "get_courses": function(frm) {
		frm.set_value("courses",[]);
        frm.set_value("students",[]);
		frappe.call({
			method: "get_courses",
			doc:frm.doc,
			callback: function(r) {
				if(r.message) {
					frm.set_value("courses", r.message.courses);
                    frm.set_value("students", r.message.students);
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