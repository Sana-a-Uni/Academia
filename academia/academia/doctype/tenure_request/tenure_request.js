// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Tenure Request", {
    refresh(frm) {

    },

    // FN: Filtering evaluations by faculty_member
    faculty_member: function (frm) {
        var faculty_member = frm.doc.faculty_member;
        if (frm.doc.evaluations) {
            frm.set_value('evaluations', '');
        }
        frm.set_query("evaluations", function () {
            return {
                filters: {
                    "faculty_member": faculty_member,
                    "workflow_state": "Approved"
                }
            };
        });
    },
    // End of the function

});
