// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Evaluation Form Generator Tool", {
    onload_post_render: function (frm) {
        frm.get_field("faculty_members").grid.set_multiple_add("faculty_member");
    },
    onload: function (frm) {
        frm.dirty();
        frm.events.employee(frm);
        frm.events.filtering_academic_term(frm);

    },
    refresh: function (frm) {
        frm.set_intro(__("Please <strong>save your changes</strong> to generate evaluation forms."), "blue");
        if (!frm.is_dirty()) {
            let button = frm.add_custom_button(__('Generate Evaluation Forms'), function () {
                generate_evaluation_forms(frm);
            });
        }
        frm.events.set_faculty_member_query(frm);
    },

    employee: function (frm) {
        frm.set_query('employee', function () {
            return {
                filters: {
                    designation: 'Department Head'
                }
            };
        });
    },

    set_faculty_member_query: function (frm) {
        let fm = [];
        for (let d in frm.doc.faculty_members) {
            if (frm.doc.faculty_members[d].faculty_member) {
                fm.push(frm.doc.faculty_members[d].faculty_member);
            }
        }

        frm.set_query("faculty_member", "faculty_members", function () {
            let filters = {
                name: ["NOT IN", fm]
            };
            if (frm.doc.department) {
                filters.department = frm.doc.department;
            }
            return {
                filters: filters
            };
        });

    },

    // FN: Clearing academic_term field when value of academic_year changes
    academic_year: function (frm) {
        if (frm.doc.academic_term) {
            frm.set_value('academic_term', '');
        }
        // Calling function
        frm.events.filtering_academic_term(frm);
    },
    // End of the function

    // FN: Filtering Academic Term field by Academic Year field
    filtering_academic_term: function (frm) {
        frm.set_query("academic_term", function () {
            return {
                filters: {
                    "academic_year": frm.doc.academic_year
                }
            };
        });
    },
    // End of the function
});

frappe.ui.form.on("Faculty Member Evaluation Form", {
    faculty_member: function (frm) {
        frm.events.set_faculty_member_query(frm);
    }
});

function generate_evaluation_forms(frm) {
    let faculty_member_names = [];
    let completed_requests = 0;
    let total_requests = frm.doc.faculty_members.length;

    if (total_requests === 0) {
        frappe.msgprint(__('No data in faculty members table to generate evaluation forms.'));
        return;
    }

    frm.doc.faculty_members.forEach((row) => {
        var data = {
            naming_series: "EVAL-FM-EMP-.department.-.evaluatee_party_name.-.YYYY.-",
            evaluatee_party_type: "Faculty Member",
            evaluator_party_type: "Employee",
            evaluator_party: frm.doc.employee,
            evaluator_party_name: frm.doc.employee_name,
            template: frm.doc.evaluation_template,
            academic_term: frm.doc.academic_term,
            academic_year: frm.doc.academic_year,
            evaluatee_party: row.faculty_member,
            evaluatee_party_name: row.faculty_member_name,
            email: row.email,
            department: row.department,
            company: row.company,
            faculty: row.faculty,
            academic_rank: row.academic_rank,
        };

        frappe.call({
            method: "frappe.client.insert",
            args: {
                doc: {
                    doctype: "Academic Evaluation",
                    ...data
                }
            },
            callback: function (response) {
                if (response.message) {
                    faculty_member_names.push(row.faculty_member_name);
                    completed_requests++;
                    if (completed_requests === total_requests) {
                        frappe.msgprint(__('Academic Evaluation created successfully for: ' + faculty_member_names.join(', ')));
                    }
                }
            }
        });
    });
}