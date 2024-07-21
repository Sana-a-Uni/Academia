// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Advertisement", {
    refresh(frm) {

    },

    onload: function (frm) {
        // Setup filtering for faculty_department based on faculty in child table
        frm.fields_dict.approved_department_needs.grid.get_field('faculty_department').get_query = function (doc, cdt, cdn) {
            let row = locals[cdt][cdn];
            return {
                filters: {
                    "faculty": row.faculty
                }
            };
        };
    },


    setup: function (frm) {
        // Changing Button Style
        $(`<style>
          .btn[data-fieldname="get_needs"] {
            background-color: #171717;
            color: white;
          }
          .btn[data-fieldname="get_needs"]:hover {
            background-color: #262626 !important;
            color: white !important;
          }
            </style>`).appendTo("head");
    },


    // Advance Get members Dialog
    get_needs: function (frm) {
        new frappe.ui.form.MultiSelectDialog({
            doctype: "Department Need Approval",
            target: frm,
            setters: {
                faculty: null,
                scientific_degree: null,
                academic_specialty: null,
                academic_year: null
            },
            get_query() {
                return {
                    filters: { docstatus: ['!=', 2] }
                }
            },
            primary_action_label: "Get Needs",

            action(selections) {
                // frm.clear_table('approved_department_needs');
                selections.forEach((need) => {
                    frappe.db.get_value("Department Need Approval", need, ["faculty", "faculty_department", "scientific_degree", "number_of_positions", "academic_specialty", "specialist_field", "academic_year", "name"], (data) => {
                        if (data) {
                            frm.events.remove_empty_row(frm);
                            frm.add_child("approved_department_needs", {
                                faculty: data.faculty,
                                faculty_department: data.faculty_department,
                                scientific_degree: data.scientific_degree,
                                number_of_positions: data.number_of_positions,
                                academic_specialty: data.academic_specialty,
                                specialist_field: data.specialist_field,
                                academic_year: data.academic_year,
                                reference_to_department_need_approval: data.name
                            });
                            frm.refresh_field("approved_department_needs");
                        }
                    });
                });
                this.dialog.hide();
            }
        });
    },
    remove_empty_row(frm) {
        if (frm.doc.approved_department_needs.length && !frm.doc.approved_department_needs[0].faculty) {
            frm.clear_table("approved_department_needs");
        }
    },
});

frappe.ui.form.on("Approved Department Need", {
    // FN: Clearing faculty_department field when value of faculty changes in child table
    faculty: function (frm, cdt, cdn) {
        let child_row = locals[cdt][cdn];
        if (child_row.faculty_department) {
            frappe.model.set_value(cdt, cdn, 'faculty_department', '');
        }
        // Setting the filtering for faculty_department based on the new faculty value
        frm.fields_dict.approved_department_needs.grid.get_field('faculty_department').get_query = function (doc, cdt, cdn) {
            return {
                filters: {
                    "faculty": child_row.faculty
                }
            };
        };
        frm.refresh_field('approved_department_needs');
    }
});
