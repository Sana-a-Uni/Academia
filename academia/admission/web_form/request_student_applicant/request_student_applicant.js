frappe.ready(function() {
	// bind events here
})

frappe.web_form.on('Student Applicant', {
    program_degree: function(frm) {
        var program_degree = frm.doc.program_degree;
        var academic_program = frm.doc.academic_program;

        frm.set_query("academic_program", function() {
            return {
                "filters": {
                    "program_degree": program_degree
                }
            };
        });

        if (frm.doc.program_degree) {
            fetchQualifications(frm, program_degree);
            fetchDocuments(frm, program_degree);
        }
    },

    refresh: function(frm) {
        var academic_program = frm.doc.academic_program;
        frm.set_query("course_code", "remedial_materials", function() {
            return {
                "filters": {
                    "program": academic_program
                }
            };
        });

        if (frm.doc.docstatus === 0) {
            if (frm.doc.status === 'Draft') {
                addStatusButton(frm, 'Verification', 'Verification');
            }
            if (frm.doc.status === "Verification") {
                addStatusButton(frm, 'Accepted', 'Accepted');
            }
            if (frm.doc.status === 'Verification' || frm.doc.status === 'Draft') {
                addRejectButton(frm);
            }
        }
    },
});

function fetchQualifications(frm, program_degree) {
    frappe.call({
        method: 'academia.admission.doctype.student_applicant.student_applicant.select_data',
        args: { condition_value: program_degree },
        callback: function(r) {
            frm.clear_table("qualification");
            r.message.forEach(function(row) {
                var child = frm.add_child("qualification");
                child.name1 = row.qualification_type;
            });
            frm.refresh_field("qualification");
        }
    });
}

function fetchDocuments(frm, program_degree) {
    frappe.call({
        method: 'academia.admission.doctype.student_applicant.student_applicant.get_document',
        args: { condition_value: program_degree },
        callback: function(r) {
            frm.clear_table("document");
            r.message.forEach(function(row) {
                var child = frm.add_child("document");
                child.name1 = row.document_type;
            });
            frm.refresh_field("document");
        }
    });
}

function addStatusButton(frm, label, status) {
    frm.add_custom_button(__(label), function() {
        frappe.call({
            method: 'academia.admission.doctype.student_applicant.student_applicant.update_statues',
            args: {
                condition_value: frm.doc.name,
                status: status
            },
            callback: function() {
                frappe.show_alert({
                    message: __('The status was successfully changed to ' + label),
                    indicator: 'green'
                });
                frm.reload_doc();
                setTimeout(function() {
                    frm.reload_doc();
                }, 1000);
            }
        });
    }, __('Status'));
}

function addRejectButton(frm) {
    frm.add_custom_button(__('Rejected'), function() {
        let d = new frappe.ui.Dialog({
            title: 'Reject Student Application',
            fields: [
                { label: 'Rejection Reason', fieldname: 'rejection_reason', fieldtype: 'Small Text', reqd: 1 },
                { label: 'Email Subject', fieldname: 'email_subject', fieldtype: 'Data', default: 'Your Application Status', reqd: 1 },
                { label: 'Email Message', fieldname: 'email_message', fieldtype: 'Text', reqd: 1 }
            ],
            primary_action_label: 'Send Email',
            primary_action(values) {
                frappe.call({
                    method: 'academia.admission.doctype.student_applicant.student_applicant.reject_student_application',
                    args: {
                        docname: frm.doc.name,
                        rejection_reason: values.rejection_reason,
                        email_subject: values.email_subject,
                        email_message: values.email_message
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.show_alert({
                                message: __('The status was successfully changed to Rejected and email sent'),
                                indicator: 'red'
                            });
                            d.hide();
                            frm.reload_doc();
                        }
                    }
                });
            }
        });
        d.show();
    }, __('Status'));
}

frappe.web_form.listview_settings = {
    add_fields: ['status'],
    get_indicator: function(doc) {
        if (doc.status === 'Accepted') {
            return [__('Accepted'), 'green', 'status,=,Accepted'];
        } else if (doc.status === 'Rejected') {
            return [__('Rejected'), 'red', 'status,=,Rejected'];
        } else if (doc.status === 'Verification') {
            return [__('Verification'), 'orange', 'status,=,Verification'];
        }
    }
};
