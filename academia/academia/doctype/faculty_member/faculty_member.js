// Copyright (c) 2023, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Faculty Member", {
    // Start of refresh event
    refresh(frm) {
        // FN: refresh fetched field 'employment_type'
        frappe.db.get_value("Employee", frm.doc.employee, "employment_type", function (value) {
            if (value && value.employment_type) {
                frm.doc.employment_type = value.employment_type;
            }
            frm.refresh_field('employment_type');
        });
        // End of the function

    },
    // End of refresh event

    // Start of validate event
    validate: function (frm) {
        // Calling functions
        frm.events.validate_extension(frm);
        frm.events.validate_child_extension(frm, 'faculty_member_academic_ranking', 'attachment', "Attachment File");
        frm.events.validate_child_extension(frm, 'faculty_member_training_course', 'certification', "Certification File");

    },
    // End of validate event

    // FN: validate 'decision_attachment' extensions
    validate_extension: function (frm) {
        var decision_attachment = frm.doc.decision_attachment;
        if (decision_attachment) {
            var allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg'];
            var decision_attachment_extension = decision_attachment.split('.').pop().toLowerCase();
            if (!allowed_extensions.includes('.' + decision_attachment_extension)) {
                frappe.throw("Decision Attachment File has an invalid extension. Only files with extensions " + allowed_extensions.join(', ') + " are allowed.");
                frappe.validated = false;
            }
        }
    },
    // End of the function

    // FN: validate file extensions of child tables
    validate_child_extension: function (frm, child_table_name, attachment_field_name, error_message) {
        if (frm.doc[child_table_name]) {
            frm.doc[child_table_name].forEach(function (row) {
                if (row[attachment_field_name]) {
                    var allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg'];
                    var attachment_extension = row[attachment_field_name].split('.').pop().toLowerCase();
                    if (!allowed_extensions.includes('.' + attachment_extension)) {
                        frappe.throw(error_message + ' ' + row[attachment_field_name] + " has an invalid extension. Only files with extensions " + allowed_extensions.join(', ') + " are allowed.");
                        frappe.validated = false;
                    }
                }
            });
        }
    },
    // End of the function

});
// // End of standard form scripts

// frappe.ui.form.on('Faculty Member', {
//     refresh: function(frm) {
//         if (frm.doc.date_of_joining_in_university && frm.doc.tenure_status === 'On Probation') {
//             console.log("Conditions met, making server call");
//             frappe.call({
//                 method: 'academia.academia.doctype.faculty_member.faculty_member.get_probation_end_date',
//                 args: {
//                     date_of_joining_in_university: frm.doc.date_of_joining_in_university,
//                     academic_rank: frm.doc.academic_rank
//                 },
//                 callback: function(r) {
//                     if (r.message) {
//                         frm.set_value('probation_period_end_date', r.message.probation_period_end_date);
//                         frm.set_value('is_eligible_for_granting_tenure', r.message.is_eligible_for_granting_tenure);
//                     }
//                 }
//             });
//         }
//     }
// });



