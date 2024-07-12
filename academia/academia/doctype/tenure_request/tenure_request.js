// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Tenure Request", {
    refresh(frm) {

    },

    // Start of onload event
    onload(frm) {
        // Calling functions
        frm.events.filtering_evaluations(frm);
    },
    // End of onload event


    // FN: Clearing evaluations when value of faculty_member changes
    faculty_member: function (frm) {
        if (frm.doc.evaluations) {
            frm.set_value('evaluations', '');
        }
        // Calling function
        frm.events.filtering_evaluations(frm);
    },
    // End of the function

    // FN: Filtering evaluations by faculty_member and workflow_state
    filtering_evaluations: function (frm) {
        frm.set_query("evaluations", function () {
            return {
                filters: {
                    "faculty_member": frm.doc.faculty_member,
                    "workflow_state": "Approved"
                }
            };
        });
    },
    // End of the function

});
