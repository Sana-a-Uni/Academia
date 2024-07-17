// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Department Need", {

    // Start of refresh event
    refresh: function (frm) {
        // Check if the record is saved
        if (!frm.doc.__islocal) {
            // Check if the user has the 'Faculty Dean' role
            if (frappe.user_roles.includes('Faculty Dean')) {
                frm.add_custom_button(__('Department Need Approval'), function () {
                    // Calling function
                    frm.events.create_department_need_approval(frm);
                }, __('Create'));
            }
        }
    },
    // End of refresh event


    // Start of onload event
    onload(frm) {
        // Calling function
        frm.events.filtering_faculty_department(frm);
    },
    // End of onload event

    // FN: Creating a new Department Need Approval doc
    create_department_need_approval: function (frm) {
        var data = {
            faculty: frm.doc.faculty,
            faculty_department: frm.doc.faculty_department,
            scientific_degree: frm.doc.scientific_degree,
            number_of_positions: frm.doc.number_of_positions,
            academic_specialty: frm.doc.academic_specialty,
            specialist_field: frm.doc.specialist_field,
            academic_year: frm.doc.academic_year,
            reference_to_department_need: frm.doc.name
        };
        // Open a new form with pre-filled data
        frappe.new_doc("Department Need Approval", data);
    },
    // End of the function


    // FN: Clearing faculty_department field when value of faculty changes
    faculty: function (frm) {
        if (frm.doc.faculty_department) {
            frm.set_value('faculty_department', '');
        }
        // Calling function
        frm.events.filtering_faculty_department(frm);
    },
    // End of the function

    // FN: Filtering faculty_department field by faculty field
    filtering_faculty_department: function (frm) {
        frm.set_query("faculty_department", function () {
            return {
                filters: {
                    "faculty": frm.doc.faculty
                }
            };
        });
    },
    // End of the function
});