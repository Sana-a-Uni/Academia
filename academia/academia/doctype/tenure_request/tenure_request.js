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
        let department = frm.doc.department;
        if (faculty_member) {
            frappe.call({
                method: 'academia.academia.doctype.tenure_request.tenure_request.get_evaluations',
                args: { faculty_member: faculty_member, department: department },
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

    // FN: validate 'attachment' extensions
    attachment: function (frm) {
        var attachment = frm.doc.attachment;
        if (attachment) {
            var allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg'];
            var attachment_extension = attachment.split('.').pop().toLowerCase();
            if (!allowed_extensions.includes('.' + attachment_extension)) {
                frm.doc.attachment = null; // Clear the attachment field
                frm.refresh_field('attachment');
                frappe.throw(__("Attachment File has an invalid extension. Only files with extensions {0} are allowed.", [allowed_extensions.join(', ')])); frappe.validated = false;
            } else {
                frappe.validated = true;
            }
        }
    },
    // End of the function

    on_submit: function (frm) {
        //applicant_type: "Student","Employee","User","Academic"
        applicants = [
            { applicant_type: "Faculty Member", applicant: frm.doc.faculty_member, applicant_name: frm.doc.faculty_member_name }
        ];
        applicants = JSON.stringify(applicants);
        frappe.call({
            method: "academia.transaction_management.doctype.transaction.transaction.create_transaction",
            args: {
                priority: "",
                title: "Tenure Request",
                category: "Faculty Member",
                sub_category: "Tenure Request",
                refrenced_document: frm.doc.name,
                applicants_list: applicants,


            },
            callback: function (r) {
                console.log(r); // Log the response object to the console for debugging

                // Check if the response contains the 'message' property
                if (r && r.message) {
                    // Access the transaction ID from the response
                    const transactionId = r.message;
                    // frappe.msgprint("Transaction ID: " + transactionId);

                    frm.set_value("referenced_transaction", transactionId);
                    go_to_transaction(transactionId, applicants, frm)

                } else {
                    console.error("Unexpected response format");
                }
            }
        });



    }

});
