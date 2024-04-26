// // Copyright (c) 2024, SanU and contributors
// // For license information, please see license.txt

frappe.ui.form.on("Academic Publication", {
    refresh(frm) {

    },

    // FN: Verifying 'publication_file' extensions
    validate: function (frm) {
        // Get the field
        var publication_file = frm.doc.publication_file;
        // Verifying that field has non-null value
        if (publication_file) {
            // Define allowed file extensions list
            var allowed_extensions = ['.pdf', '.txt', '.doc', '.docx', '.ppt', '.pptx'];
            // Get the file extension of 'publication_file' field
            var publication_file_extension = publication_file.split('.').pop().toLowerCase();
            // Check if the file extension of 'publication_file' field is allowed
            if (!allowed_extensions.includes('.' + publication_file_extension)) {
                frappe.throw("Publication File has an invalid extension. Only files with extensions " + allowed_extensions.join(', ') + " are allowed.");
                frappe.validated = false;
            }
        }
    }
});
