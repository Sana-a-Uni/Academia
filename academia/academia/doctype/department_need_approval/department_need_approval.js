// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Department Need Approval", {
	refresh(frm) {

	},

    // Start of onload event
    onload(frm) {
        // Calling functions
        frm.events.filtering_faculty_department(frm);
    },
    // End of onload event

    // FN: Clearing faculty_department field when value of faculty changes
    faculty: function (frm) {
        if (frm.doc.faculty_department) {
            frm.set_value('faculty_department', '');
        }
        // Calling function
        frm.events.filtering_faculty_department(frm);
    },
    // End of the function

    // FN: Filtering faculty_department field by faculty field
    filtering_faculty_department: function (frm) {
        frm.set_query("faculty_department", function () {
            return {
                filters: {
                    "faculty": frm.doc.faculty
                }
            };
        });
    },
    // End of the function
});
