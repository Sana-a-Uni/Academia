// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Evaluation Form Generator Tool", {
    setup: function (frm) {
        // Changing Button Style
        $(`<style>
          .btn[data-fieldname="get_faculty_members"] {
            background-color: #171717;
            color: white;
          }
          .btn[data-fieldname="get_faculty_members"]:hover {
            background-color: #262626 !important;
            color: white !important;
          }
            </style>`).appendTo("head");

        frm.get_field("faculty_members").grid.cannot_add_rows = true;
    },


    onload: function (frm) {
        frm.dirty();
        frm.events.filtering_academic_term(frm);
        frm.events.set_section_label(frm);
    },

    refresh: function (frm) {
        frm.set_intro(__("Please <strong>save your changes</strong> to generate evaluation forms."), "blue");
        if (!frm.is_dirty()) {
            if (frm.doc.evaluation_type === "Department Head Evaluate his Faculty Members") {
                frm.add_custom_button(__('Generate Evaluation Forms'), function () {
                    generate_evaluation_forms(
                        frm,
                        "EVAL-FM-EMP-.department.-.evaluatee_party_name.-.YYYY.-",
                        "Faculty Member",
                        "Employee"
                    );
                });
            } else if (frm.doc.evaluation_type === "Faculty Members Evaluate their Department Head") {
                frm.add_custom_button(__('Generate Evaluation Forms'), function () {
                    generate_evaluation_forms(
                        frm,
                        "EVAL-EMP-FM-.department.-.evaluatee_party_name.-.YYYY.-",
                        "Employee",
                        "Faculty Member"
                    );
                });
            } else if (frm.doc.evaluation_type === "Faculty Members Evaluate Employee") {
                frm.add_custom_button(__('Generate Evaluation Forms'), function () {
                    generate_evaluation_forms(
                        frm,
                        "EVAL-EMP-FM-.department.-.evaluatee_party_name.-.YYYY.-",
                        "Employee",
                        "Faculty Member"
                    );
                });
            }
        }
        frm.events.set_faculty_member_query(frm);
    },

    filtering_department_head: function (frm) {
        if (frm.doc.evaluation_type === "Faculty Members Evaluate their Department Head" || frm.doc.evaluation_type === "Department Head Evaluate his Faculty Members") {
            frm.set_query('employee', function () {
                return {
                    filters: {
                        designation: 'Department Head'
                    }
                };
            });
        } else {
            frm.set_query('employee', function () {
                return {};
            });
        }
    },

    employee: function (frm) {
        if (frm.doc.evaluation_type === "Faculty Members Evaluate their Department Head" || frm.doc.evaluation_type === "Department Head Evaluate his Faculty Members") {
            let department = frm.doc.department;
            if (department) {
                frappe.call({
                    method: 'academia.academia.doctype.evaluation_form_generator_tool.evaluation_form_generator_tool.get_faculty_members_from_department',
                    args: { department: department },
                }).done((r) => {
                    frm.doc.faculty_members = [];
                    $.each(r.message, function (_i, e) {
                        let entry = frm.add_child("faculty_members");
                        entry.faculty_member = e.name;
                    });
                    frm.refresh_field("faculty_members");
                });
            } else {
                frm.clear_table('faculty_members');
                frm.refresh_field("faculty_members");
            }
        } else if (frm.doc.evaluation_type === "Faculty Members Evaluate Employee") {
            let company = frm.doc.company;
            if (company) {
                frappe.call({
                    method: 'academia.academia.doctype.evaluation_form_generator_tool.evaluation_form_generator_tool.get_faculty_members_from_company',
                    args: { company: company },
                }).done((r) => {
                    frm.doc.faculty_members = [];
                    $.each(r.message, function (_i, e) {
                        let entry = frm.add_child("faculty_members");
                        entry.faculty_member = e.name;
                    });
                    frm.refresh_field("faculty_members");
                });
            }
        }
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
            if (frm.doc.evaluation_type !== "Faculty Members Evaluate Employee" && frm.doc.department) {
                filters.department = frm.doc.department;
            }
            return {
                filters: filters
            };
        });
    },

    academic_year: function (frm) {
        if (frm.doc.academic_term) {
            frm.set_value('academic_term', '');
        }
        frm.events.filtering_academic_term(frm);
    },

    filtering_academic_term: function (frm) {
        frm.set_query("academic_term", function () {
            return {
                filters: {
                    "academic_year": frm.doc.academic_year
                }
            };
        });
    },

    evaluation_type: function (frm) {
        frm.events.filtering_department_head(frm);
        frm.events.set_section_label(frm);
        frm.events.clear_fields_data(frm);
        frm.events.clear_faculty_members(frm); // Ensure this line is being executed
    },

    clear_fields_data: function (frm) {
        if (frm.doc.employee) {
            frm.set_value('employee', '');
        }
    },

    clear_faculty_members: function (frm) {
        // Clear the faculty_members table
        frm.clear_table('faculty_members');
        frm.refresh_field('faculty_members'); // Refresh the field to ensure it's updated
    },

    set_section_label: function (frm) {
        var first_section_label = "";
        var second_section_label = "";
        if (frm.doc.evaluation_type === "Department Head Evaluate his Faculty Members") {
            first_section_label = "Evaluator";
            second_section_label = "Evaluatee";
        } else if (frm.doc.evaluation_type === "Faculty Members Evaluate their Department Head") {
            first_section_label = "Evaluatee";
            second_section_label = "Evaluator";
        } else if (frm.doc.evaluation_type === "Faculty Members Evaluate Employee") {
            first_section_label = "Evaluatee";
            second_section_label = "Evaluator";
        }
        // jQuery code to change the label of Section Break
        $('div[data-fieldname="first_section"] .section-head').text(first_section_label);
        $('div[data-fieldname="second_section"] .section-head').text(second_section_label);
        frm.refresh_field('first_section');
        frm.refresh_field('second_section');
    },

    clear_faculty_members: function (frm) {
        frm.clear_table("faculty_members");
        frm.refresh_field("faculty_members");
    },

    get_faculty_members: function (frm) {
        var setters = {
            company: frm.doc.company,
            department: null,
        };

        let existingMembers = frm.doc.faculty_members || [];
        let existingMembersIds = existingMembers.map(r => r.faculty_member);

        let Dialog = new frappe.ui.form.MultiSelectDialog({
            doctype: "Faculty Member",
            target: frm,
            setters: setters,

            // add_filters_group: 1,
            date_field: "fm_date",

            get_query() {
                let filters = {
                    docstatus: ['!=', 2],
                    company: ['!=', null],
                    department: ['!=', null],
                    name: ['not in', existingMembersIds], // don't show Employee of current user

                };

                return {
                    filters: filters
                };
            },

            primary_action_label: "Get Faculty Members",
            action(selections) {

                // Fetch the selected employees with specific fields
                frappe.call({
                    method: "frappe.client.get_list",
                    args: {
                        doctype: "Faculty Member",
                        filters: { name: ["in", selections] },
                        fields: ["name", "faculty_member_name", "academic_rank", "company", "faculty", "department", "email"]
                    },

                    callback: (response) => {
                        var selectedMembers = response.message;

                        selectedMembers.forEach((member) => {
                            frm.add_child("faculty_members", {
                                faculty_member: member.name,
                                faculty_member_name: member.faculty_member_name,
                                academic_rank: member.academic_rank,
                                company: member.company,
                                faculty: member.faculty,
                                department: member.department,
                                email: member.email,
                            })
                        })

                        this.dialog.hide();
                        frm.refresh_field("faculty_members");
                    }
                });
            }
        });
    },

});

frappe.ui.form.on("Faculty Member Evaluation Form", {
    faculty_member: function (frm) {
        frm.events.set_faculty_member_query(frm);
    }
});

function generate_evaluation_forms(frm, naming_series, evaluatee_party_type, evaluator_party_type) {
    let faculty_member_names = [];
    let completed_requests = 0;
    let total_requests = frm.doc.faculty_members.length;

    if (total_requests === 0) {
        frappe.msgprint(__('No data in faculty members table to generate evaluation forms.'));
        return;
    }

    frm.doc.faculty_members.forEach((row) => {
        var data = {
            naming_series: naming_series,
            evaluatee_party_type: evaluatee_party_type,
            evaluator_party_type: evaluator_party_type,
            template: frm.doc.evaluation_template,
            academic_term: frm.doc.academic_term,
            academic_year: frm.doc.academic_year,
        };

        if (frm.doc.evaluation_type === "Department Head Evaluate his Faculty Members") {
            data.evaluator_party = frm.doc.employee;
            data.evaluator_party_name = frm.doc.employee_name;
            data.evaluatee_party = row.faculty_member;
            data.evaluatee_party_name = row.faculty_member_name;
            data.email = row.email;
            data.department = row.department;
            data.company = row.company;
            data.faculty = row.faculty;
            data.academic_rank = row.academic_rank;

        } else if (frm.doc.evaluation_type === "Faculty Members Evaluate their Department Head" || frm.doc.evaluation_type === "Faculty Members Evaluate Employee") {
            data.evaluator_party = row.faculty_member;
            data.evaluator_party_name = row.faculty_member_name;
            data.evaluatee_party = frm.doc.employee;
            data.evaluatee_party_name = frm.doc.employee_name;
            data.company = frm.doc.company;
            data.department = frm.doc.department;
            data.designation = frm.doc.designation;
            data.email = frm.doc.email;
        }
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
                        frappe.msgprint(__('Academic Evaluation created successfully for: ') + faculty_member_names.join(', '));
                    }
                }
            }
        });
    });
}
