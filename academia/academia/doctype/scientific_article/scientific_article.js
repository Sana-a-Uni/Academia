// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

// Start of standard form scripts
frappe.ui.form.on("Scientific Article", {
    refresh(frm) {

    },
});
// End of standard form scripts

// --- Start of 'scientific_article_author' childe table form scripts ---
frappe.ui.form.on('Academic Author', {
    // FN: filter duplicate 'author_name' field in 'scientific_article_author' child table
    scientific_article_author_add: function (frm) {
        frm.fields_dict['scientific_article_author'].grid.get_field('author_name').get_query = function (doc) {
            let author_list = [];
            if (!doc.__islocal) author_list.push(doc.author_name);
            $.each(doc.scientific_article_author, function (idx, val) {
                if (val.author_name) author_list.push(val.author_name);
            });
            return { filters: [['Faculty Member', 'name', 'not in', author_list]] };
        };
    },
    // End of the function

});
// End of childe table form scripts

