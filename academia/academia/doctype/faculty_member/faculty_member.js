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

    // Start of onload event
    onload(frm) {
        // Calling functions
        frm.events.filtering_faculty(frm);
    },
    // End of onload event

    // Start of validate event
    validate: function (frm) {
        // Calling functions
        frm.events.validate_extension(frm);
        frm.events.validate_child_extension(frm, 'faculty_member_academic_ranking', 'attachment', "Attachment File");
        frm.events.validate_child_extension(frm, 'faculty_member_training_course', 'certification', "Certification File");
        frm.events.validate_date(frm);
    },
    // End of validate event

    // FN: validate 'decision_attachment' extensions
    validate_extension: function (frm) {
        var decision_attachment = frm.doc.decision_attachment;
        if (decision_attachment) {
            var allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg'];
            var decision_attachment_extension = decision_attachment.split('.').pop().toLowerCase();
            if (!allowed_extensions.includes('.' + decision_attachment_extension)) {
                frappe.throw(__("Decision File has an invalid extension. Only files with extensions {0} are allowed.", [allowed_extensions.join(', ')]));
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

    // FN: validate dates of child tables
    validate_date: function (frm) {
        const today = frappe.datetime.get_today();
        frm.doc['faculty_member_training_course'].forEach(function (row) {
            if (row.starts_on) {
                if (row.starts_on > today) {
                    frappe.throw(__('Start date in training courses table cannot be in the future.'));
                }
            }
            if (row.ends_on) {
                if (row.ends_on > today) {
                    frappe.throw(__('End date in training courses table cannot be in the future.'));
                }
            }
            if (row.starts_on && row.ends_on) {
                if (row.ends_on < row.starts_on) {
                    frappe.throw(__('End date in training courses table must be after the start date.'));
                }
            }
        });

        frm.doc['faculty_member_conference_and_workshop'].forEach(function (row) {
            if (row.starts_on) {
                if (row.starts_on > today) {
                    frappe.throw(__('Start date in conferences and workshops table cannot be in the future.'));
                }
            }
            if (row.ends_on) {
                if (row.ends_on > today) {
                    frappe.throw(__('End date in conferences and workshops table cannot be in the future.'));
                }
            }
            if (row.starts_on && row.ends_on) {
                if (row.ends_on < row.starts_on) {
                    frappe.throw(__('End date in conferences and workshops table must be after the start date.'));
                }
            }
        });

        frm.doc['faculty_member_university_and_community_service'].forEach(function (row) {
            if (row.date) {
                if (row.date > today) {
                    frappe.throw(__('Date in university and community services table cannot be in the future.'));
                }
            }
        });

        frm.doc['faculty_member_activity'].forEach(function (row) {
            if (row.date) {
                if (row.date > today) {
                    frappe.throw(__('Date in activities table cannot be in the future.'));
                }
            }
        });

        frm.doc['faculty_member_award_and_appreciation_certificate'].forEach(function (row) {
            if (row.date) {
                if (row.date > today) {
                    frappe.throw(__('Date in awards and appreciation certificates table cannot be in the future.'));
                }
            }
        });
    },
    // End of the function

    // FN: Clearing faculty field when value of company changes
    company: function (frm) {
        if (frm.doc.faculty) {
            frm.set_value('faculty', '');
        }
        // Calling function
        frm.events.filtering_faculty(frm);
    },
    // End of the function

    // FN: Filtering faculty field by company field
    filtering_faculty: function (frm) {
        frm.set_query("faculty", function () {
            return {
                filters: {
                    "company": frm.doc.company
                }
            };
        });
    },
    // End of the function




});
// // End of standard form scripts

frappe.ui.form.on('Faculty Member', {
    refresh: function (frm) {

    },
    from_another_university: function (frm) {

        // Get the selected university
        let selected_university = frm.doc.from_another_university;

        // Set filter for the external faculty field based on the selected university
        frm.set_query('external_faculty', function () {
            return {
                filters: {
                    university: selected_university
                }
            };
        });

        // Clear the external faculty field if the university is changed
        frm.set_value('external_faculty', null);
    }
});





