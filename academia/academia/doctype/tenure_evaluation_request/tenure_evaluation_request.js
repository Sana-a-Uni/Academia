// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Tenure Evaluation Request", {
    refresh(frm) {

    },

    // Start of validate event
    validate: function (frm) {
        // Calling functions
        frm.events.validate_extension(frm);
    },
    // End of validate event

    // FN: validate 'attachment' extensions
    validate_extension: function (frm) {
        var attachment = frm.doc.attachment;
        if (attachment) {
            var allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg'];
            var attachment_extension = attachment.split('.').pop().toLowerCase();
            if (!allowed_extensions.includes('.' + attachment_extension)) {
                frappe.throw("Attachment File has an invalid extension. Only files with extensions " + allowed_extensions.join(', ') + " are allowed.");
                frappe.validated = false;
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
    }
    // End of the function

});
