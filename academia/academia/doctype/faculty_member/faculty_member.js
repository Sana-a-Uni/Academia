// Copyright (c) 2023, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Faculty Member", {
    // refresh(frm) {

    // },
});

// Faculty Member Training Course Child DocType
frappe.ui.form.on("Faculty Member Training Course", {
    // FN: Verifying 'certification' file extensions
    validate: function (frm, cdt, cdn) {
        // Get the field
        // var certification_file = frappe.model.get_doc(cdt, cdn); // not working
        var row = locals[cdt][cdn];
        // Verifying that field has non-null value
        if (row.certification) {
            // Define allowed file extensions list
            var allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg'];
            // Get the file extension of 'certification' field
            var certification_file_extension = row.certification.split('.').pop().toLowerCase();
            // Check if the file extension of 'certification' field is allowed
            if (!allowed_extensions.includes('.' + certification_file_extension)) {
                frappe.throw("Certification file has an invalid extension. Only files with extensions " + allowed_extensions.join(', ') + " are allowed.");
                frappe.validated = false;
            }
        }
    }
});

