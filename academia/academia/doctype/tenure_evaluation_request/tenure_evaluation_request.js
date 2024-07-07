// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Tenure Evaluation Request", {
    refresh: function (frm) {

    },

    // FN: validate 'attachment' extensions
    attachment: function (frm) {
        var attachment = frm.doc.attachment;
        if (attachment) {
            var allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg'];
            var attachment_extension = attachment.split('.').pop().toLowerCase();
            if (!allowed_extensions.includes('.' + attachment_extension)) {
                frm.doc.attachment = null; // Clear the attachment field
                frm.refresh_field('attachment');
                frappe.throw("Attachment File has an invalid extension. Only files with extensions " + allowed_extensions.join(', ') + " are allowed.");
                frappe.validated = false;
            } else {
                frappe.validated = true;
            }
        }
    },
    // End of the function

    // FN: Get evaluation criteria
    template: function (frm) {
        let template = frm.doc.template;
        if (template) {
            frappe.call({
                method: 'academia.academia.doctype.tenure_evaluation_request.tenure_evaluation_request.get_evaluation_criteria',
                args: { template: template },
            }).done((r) => {
                frm.doc.tenure_evaluation_criteria = []
                $.each(r.message, function (_i, e) {
                    let entry = frm.add_child("tenure_evaluation_criteria");
                    entry.criterion = e.criterion;
                })
                refresh_field("tenure_evaluation_criteria")
            });
        }
    },
    // End of the function


    // FN: Filtering Academic Term field by Academic Year field
    academic_year: function (frm) {
        var academic_year = frm.doc.academic_year;
        if (frm.doc.academic_term) {
            frm.set_value('academic_term', '');
        }
        frm.set_query("academic_term", function () {
            return {
                filters: {
                    "academic_year": academic_year
                }
            };
        });
    },
    // End of the function

});
