// // Copyright (c) 2024, SanU and contributors
// // For license information, please see license.txt

// Start of standard form scripts
frappe.ui.form.on("Academic Publication", {
    // Start of refresh event
    refresh(frm) {
        // FN: sort child documents by'author_order'
        var order = ['First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh'];
        frm.doc.academic_publication_author.sort(function (a, b) {
            return order.indexOf(a.author_order) - order.indexOf(b.author_order);
        });
        frm.refresh_field('academic_publication_author');
        // End of the function
    },
    // End of refresh event

    // Start of validate event
    validate: function (frm) {
        // Calling functions
        frm.events.validate_extension(frm);
        frm.events.validate_duplicate_author_name(frm);
        frm.events.validate_duplicate_author_order(frm);

    },
    // End of validate event

    // FN: validate 'publication_file' extensions
    validate_extension: function (frm) {
        var publication_file = frm.doc.publication_file;
        if (publication_file) {
            var allowed_extensions = ['.pdf', '.txt', '.doc', '.docx', '.ppt', '.pptx', '.png', '.jpg', '.jpeg'];
            var publication_file_extension = publication_file.split('.').pop().toLowerCase();
            if (!allowed_extensions.includes('.' + publication_file_extension)) {
                frappe.throw("Publication File has an invalid extension. Only files with extensions " + allowed_extensions.join(', ') + " are allowed.");
                frappe.validated = false;
            }
        }
    },
    // End of the function

    // FN: validate duplicate 'author_name' field in 'academic_publication_author' child table 
    validate_duplicate_author_name: function (frm) {
        var academic_publication_author = [];
        frm.doc.academic_publication_author.forEach(function (row) {
            academic_publication_author.push(row.author_name);
        });
        var name_set = new Set(academic_publication_author);
        if (academic_publication_author.length != name_set.size) {
            frappe.throw(("Author name cannot be duplicated"));
        }
    },
    // End of the function

    // FN: validate duplicate 'author_order' field in 'academic_publication_author' child table 
    validate_duplicate_author_order: function (frm) {
        var academic_publication_author = [];
        frm.doc.academic_publication_author.forEach(function (row) {
            academic_publication_author.push(row.author_order);
        });
        var order_set = new Set(academic_publication_author);
        if (academic_publication_author.length != order_set.size) {
            frappe.throw(("Author order cannot be duplicated"));
        }
    },
    // End of the function

});
// End of standard form scripts

// --- Start of 'academic_publication_author' childe table form scripts ---
frappe.ui.form.on('Academic Author', {
    // FN: filter duplicate 'author_name' field in 'academic_publication_author' child table
    academic_publication_author_add: function (frm) {
        frm.fields_dict['academic_publication_author'].grid.get_field('author_name').get_query = function (doc) {
            let author_list = [];
            if (!doc.__islocal) author_list.push(doc.author_name);
            $.each(doc.academic_publication_author, function (idx, val) {
                if (val.author_name) author_list.push(val.author_name);
            });
            return { filters: [['Faculty Member', 'name', 'not in', author_list]] };
        };
    },
    // End of the function

});
// End of childe table form scripts