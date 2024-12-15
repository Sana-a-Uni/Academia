// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Academic Program", {
	academic_degree: function (frm) {
		if (
			frm.doc.academic_degree === "Master Degree" ||
			frm.doc.academic_degree === "PHD Degree"
		) {
			frm.toggle_display(["courses", "research_or_thesis"], true);
		} else {
			frm.toggle_display(["courses", "research_or_thesis"], false);
			frm.set_value("courses", false);
			frm.set_value("research_or_thesis", false);
		}
		frm.set_value("minimum_course_average_to_start_research", "");
		frm.set_value("minimum_research_period", "");
		frm.set_value("maximum_research_period", "");
	},
});

frappe.ui.form.on("Academic Program", "validate", function (frm) {
	if (frm.is_new()) {
		frm.trigger("academic_degree");
	}

	if (frm.doc.academic_degree !== frm.doc.__original?.academic_degree) {
		frm.set_value("courses", false);
		frm.set_value("research_or_thesis", false);
	}
});
