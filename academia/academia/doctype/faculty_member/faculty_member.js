// Copyright (c) 2023, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Faculty Member", {
    // Start of refresh event
    refresh(frm) {
        // FN: refresh fetched field 'company'
        frappe.db.get_value("Employee", frm.doc.employee, "company", function (value) {
            if (value && value.company) {
                frm.doc.company = value.company;
            }
            frm.refresh_field('company');
        });
        // End of the function
    },
    // End of refresh event

    // Start of validate event
    validate: function (frm) {
        // Calling functions
        frm.events.validate_extension(frm);
    },
    // End of validate event

    // FN: validate 'certification' file extensions
    validate_extension: function (frm) {
        frm.doc.faculty_member_training_course.forEach(function (row) {
            if (row.certification) {
                var allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg'];
                var certification_file_extension = row.certification.split('.').pop().toLowerCase();
                if (!allowed_extensions.includes('.' + certification_file_extension)) {
                    frappe.throw("Certification file " + row.certification + " has an invalid extension. Only files with extensions " + allowed_extensions.join(', ') + " are allowed.");
                    frappe.validated = false;
                }
            }
        });
    },
    // End of the function

});

