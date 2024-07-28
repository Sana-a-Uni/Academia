// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Tenure Request", {
    refresh(frm) {
        if (frm.doc.faculty_member && (!frm.doc.evaluations || frm.doc.evaluations.length === 0)) {
            frappe.throw(__("Dear {0}, there are no submitted academic evaluations associated with you.").replace("{0}", frm.doc.faculty_member_name));
        }
    },

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
        let faculty_member = frm.doc.faculty_member;
        if (faculty_member) {
            frappe.call({
                method: 'academia.academia.doctype.tenure_request.tenure_request.get_evaluations',
                args: { faculty_member: faculty_member },
            }).done((r) => {
                frm.doc.evaluations = []
                $.each(r.message, function (_i, e) {
                    let entry = frm.add_child("evaluations");
                    entry.evaluation = e.name;
                })
                refresh_field("evaluations")
            });
        }
    },

    // End of the function

});
