// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Thesis Arbitration Committee", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Internal Arbitration Committee", {
    faculty: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];

        // Clear the faculty member field when faculty changes
        frappe.model.set_value(cdt, cdn, 'faculty_member', '');
        
        // Apply filtering logic
        filter_internal(frm, cdt, cdn);
    },

    academic_rank: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        
        // Clear the faculty_member field
        frappe.model.set_value(cdt, cdn, 'faculty_member', '');
        
        // Apply filtering logic
        filter_internal(frm, cdt, cdn);
    },

    faculty_member: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        let duplicate = frm.doc.internal_arbitration_committee.some((r) => 
            r.faculty === row.faculty && 
            r.academic_rank === row.academic_rank && 
            r.faculty_member === row.faculty_member && 
            r.idx !== row.idx
        );

        if (duplicate) {
            frappe.msgprint(__('This Faculty Member is already selected. Please choose a different one.'));
            frappe.model.set_value(cdt, cdn, 'faculty_member', '');
        }
    },

    internal_arbitration_committee_add: function(frm, cdt, cdn) {
        filter_internal(frm, cdt, cdn);
    }
});

frappe.ui.form.on("External Arbitration Committee", {
    university: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        
        // Clear the faculty_member and external_faculty fields
        frappe.model.set_value(cdt, cdn, 'faculty_member', '');
        frappe.model.set_value(cdt, cdn, 'external_faculty', '');
        
        // Apply filtering logic
        filter_external(frm, cdt, cdn);
    },

    academic_rank: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        
        // Clear the faculty_member field
        frappe.model.set_value(cdt, cdn, 'faculty_member', '');
        
        // Apply filtering logic
        filter_external(frm, cdt, cdn);
    },

    external_faculty: function (frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        
        // Clear the faculty_member field
        frappe.model.set_value(cdt, cdn, 'faculty_member', '');
        
        // Apply filtering logic
        filter_external(frm, cdt, cdn);
    },

    faculty_member: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        let duplicate = frm.doc.external_arbitration_committee.some((r) => 
            r.university === row.university && 
            r.external_faculty === row.external_faculty && 
            r.academic_rank === row.academic_rank && 
            r.faculty_member === row.faculty_member && 
            r.idx !== row.idx
        );

        if (duplicate) {
            frappe.msgprint(__('This Faculty Member with the same university, external faculty, and academic rank is already selected. Please choose a different one.'));
            frappe.model.set_value(cdt, cdn, 'faculty_member', '');
        }
    },

    external_arbitration_committee_add: function(frm, cdt, cdn) {
        filter_external(frm, cdt, cdn);
    }
});

function filter_internal(frm, cdt, cdn) {
    const row = locals[cdt][cdn];
    frm.fields_dict['internal_arbitration_committee'].grid.get_field('faculty_member').get_query = function () {
        let filters = {
            'from_another_university': "",
            'external_faculty': ""
        };

        if (row.faculty) {
            filters['faculty'] = row.faculty;
        }

        if (row.academic_rank) {
            filters['academic_rank'] = row.academic_rank;
        }

        return { filters: filters };
    };
}

function filter_external(frm, cdt, cdn) {
    const row = locals[cdt][cdn];

    frm.fields_dict['external_arbitration_committee'].grid.get_field('faculty_member').get_query = function () {
        let filters = {};

        if (row.university) {
            filters['from_another_university'] = row.university;
        } else {
            filters['from_another_university'] = ['!=', ''];
        }

        if (row.external_faculty) {
            filters['external_faculty'] = row.external_faculty;
        } else {
            filters['external_faculty'] = ['!=', ''];
        }

        if (row.academic_rank) {
            filters['academic_rank'] = row.academic_rank;
        }

        return { filters: filters };
    };

    frm.fields_dict['external_arbitration_committee'].grid.get_field('external_faculty').get_query = function () {
        let filters = {};

        if (row.university) {
            filters['university'] = row.university;
        }

        return { filters: filters };
    };
}


