// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("University Academic Calendar", {
	refresh: function (frm) {
		frm.fields_dict["academic_calendar_term_one"].grid.get_field("procedure").get_query =
			function (doc, cdt, cdn) {
				let selected_procedures = frm.doc.academic_calendar_term_one.map(
					(row) => row.procedure
				);
				return {
					filters: [["name", "not in", selected_procedures]],
				};
			};
		frm.fields_dict["academic_calendar_term_two"].grid.get_field("procedure").get_query =
			function (doc, cdt, cdn) {
				let selected_procedures = frm.doc.academic_calendar_term_two.map(
					(row) => row.procedure
				);
				return {
					filters: [["name", "not in", selected_procedures]],
				};
			};
		frm.fields_dict["academic_calendar_term_three"].grid.get_field("procedure").get_query =
			function (doc, cdt, cdn) {
				let selected_procedures = frm.doc.academic_calendar_term_one.map(
					(row) => row.procedure
				);
				return {
					filters: [["name", "not in", selected_procedures]],
				};
			};
	},
});
