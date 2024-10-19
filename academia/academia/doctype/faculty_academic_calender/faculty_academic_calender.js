// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Faculty Academic Calender", {
	// get university calendar for term one
	get_university_calendar_term_one: function (frm) {
		frm.set_value("academic_calendar_term_one", []);
		frappe.call({
			method: "get_university_calendar_term_one",
			doc: frm.doc,
			callback: function (r) {
				if (r.message) {
					frm.set_value("academic_calendar_term_one", r.message);
				}
			},
		});
	},

	// get university calendar for term two
	get_university_calendar_term_two: function (frm) {
		frm.set_value("academic_calendar_term_two", []);
		frappe.call({
			method: "get_university_calendar_term_two",
			doc: frm.doc,
			callback: function (r) {
				if (r.message) {
					frm.set_value("academic_calendar_term_two", r.message);
				}
			},
		});
	},

	// get university calendar for term three
	get_university_calendar_term_three: function (frm) {
		frm.set_value("academic_calendar_term_three", []);
		frappe.call({
			method: "get_university_calendar_term_three",
			doc: frm.doc,
			callback: function (r) {
				if (r.message) {
					frm.set_value("academic_calendar_term_three", r.message);
				}
			},
		});
	},
});
