// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Academic Evaluation", {
    refresh: function (frm) {
        frm.events.set_options(frm);
    },

    // Start of onload event
    onload(frm) {
        // Calling functions
        frm.events.filtering_academic_term(frm);
        // frm.events.template(frm);
        update_party_field_label(frm, 'evaluatee_party_type', 'evaluatee_party');
        update_party_name_field_label(frm, 'evaluatee_party_type', 'evaluatee_party_name');
        update_party_field_label(frm, 'evaluator_party_type', 'evaluator_party');
        update_party_name_field_label(frm, 'evaluator_party_type', 'evaluator_party_name');
        
    },
    // End of onload event


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

    // FN: Get evaluation criteria
    template: function (frm) {
        let template = frm.doc.template;
        if (template) {
            frappe.call({
                method: 'academia.academia.doctype.academic_evaluation.academic_evaluation.get_evaluation_criteria',
                args: { template: template },
            }).done((r) => {
                frm.doc.evaluation_details = []
                $.each(r.message, function (_i, e) {
                    let entry = frm.add_child("evaluation_details");
                    entry.criterion = e.criterion;
                })
                refresh_field("evaluation_details");
            });
        } else {
            frm.clear_table('evaluation_details');
            refresh_field("evaluation_details");
        }
    },
    // End of the function

    // FN: validate 'attachment' extensions
    attachment: function (frm) {
        var attachment = frm.doc.attachment;
        if (attachment) {
            var allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg'];
            var attachment_extension = attachment.split('.').pop().toLowerCase();
            if (!allowed_extensions.includes('.' + attachment_extension)) {
                frm.doc.attachment = null; // Clear the attachment field
                frm.refresh_field('attachment');
                frappe.throw(__("Attachment File has an invalid extension. Only files with extensions {0} are allowed.", [allowed_extensions.join(', ')]));
                frappe.validated = false;
            } else {
                frappe.validated = true;
            }
        }
    },
    // End of the function


    // FN: Clearing academic_term field when value of academic_year changes
    evaluatee_party_type: function (frm) {
        if (frm.doc.evaluatee_party) {
            frm.set_value('evaluatee_party', '');
        }

        // Calling function
        update_party_field_label(frm, 'evaluatee_party_type', 'evaluatee_party');
        update_party_name_field_label(frm, 'evaluatee_party_type', 'evaluatee_party_name');
        update_naming_series(frm);
    },
    // End of the function

    evaluator_party_type: function (frm) {
        if (frm.doc.evaluator_party) {
            frm.set_value('evaluator_party', '');
        }

        update_party_field_label(frm, 'evaluator_party_type', 'evaluator_party');
        update_party_name_field_label(frm, 'evaluator_party_type', 'evaluator_party_name');
        update_naming_series(frm);
    },

    // FN: 
    set_options: function (frm) {
        var evaluatee_options = ['Employee', 'Faculty Member'];
        frm.set_df_property('evaluatee_party_type', 'options', evaluatee_options.join('\n'));
        frm.refresh_field('evaluatee_party_type');
        var evaluator_options = ['Employee', 'Faculty Member', 'Student'];
        frm.set_df_property('evaluator_party_type', 'options', evaluator_options.join('\n'));
        frm.refresh_field('evaluator_party_type');
    },
    // End of the function


    evaluator_party: function (frm) {
        if (frm.doc.evaluator_party) {
            fetch_party_name(frm, frm.doc.evaluator_party_type, 'evaluator_party', 'evaluator_party_name', 'employee_name', 'faculty_member_name', 'first_name');
        } else {
            frm.set_value('evaluator_party_name', 'None');
        }
    },

    evaluatee_party: function (frm) {
        clear_evaluatee_information(frm);
        if (frm.doc.evaluatee_party) {
            fetch_party_name(frm, frm.doc.evaluatee_party_type, 'evaluatee_party', 'evaluatee_party_name', 'employee_name', 'faculty_member_name', 'first_name');
            fetch_evaluatee_information(frm, frm.doc.evaluatee_party_type, frm.doc.evaluatee_party);
        } else {
            frm.set_value('evaluatee_party_name', 'None');
        }
    },

});


function update_party_field_label(frm, partyTypeField, partyField) {
    var party_type = frm.doc[partyTypeField];
    var party_label = "";
    if (party_type === 'Employee') {
        party_label = "Employee";
    } else if (party_type === 'Faculty Member') {
        party_label = "Faculty Member";
    } else if (party_type === 'Student') {
        party_label = "Student";
    } else {
        party_label = "Party";
    }

    frm.set_df_property(partyField, 'label', party_label);
    frm.refresh_field(partyField);
}


function update_naming_series(frm) {
    var naming_series = '';
    if (frm.doc.evaluatee_party_type == 'Employee' && frm.doc.evaluator_party_type == 'Employee') {
        naming_series = 'EVAL-EMP-EMP-.department.-.evaluatee_party_name.-.YYYY.-';
    } else if (frm.doc.evaluatee_party_type == 'Employee' && frm.doc.evaluator_party_type == 'Faculty Member') {
        naming_series = 'EVAL-EMP-FM-.department.-.evaluatee_party_name.-.YYYY.-';
    } else if (frm.doc.evaluatee_party_type == 'Employee' && frm.doc.evaluator_party_type == 'Student') {
        naming_series = 'EVAL-EMP-STD-.department.-.evaluatee_party_name.-.YYYY.-';
    } else if (frm.doc.evaluatee_party_type == 'Faculty Member' && frm.doc.evaluator_party_type == 'Employee') {
        naming_series = 'EVAL-FM-EMP-.department.-.evaluatee_party_name.-.YYYY.-';
    } else if (frm.doc.evaluatee_party_type == 'Faculty Member' && frm.doc.evaluator_party_type == 'Faculty Member') {
        naming_series = 'EVAL-FM-FM-.department.-.evaluatee_party_name.-.YYYY.-';
    } else if (frm.doc.evaluatee_party_type == 'Faculty Member' && frm.doc.evaluator_party_type == 'Student') {
        naming_series = 'EVAL-FM-STD-.department.-.evaluatee_party_name.-.YYYY.-';
    } else {
        naming_series = 'Unknown-';
    }

    frm.set_value('naming_series', naming_series);
}


function update_party_name_field_label(frm, partyTypeField, partyNameField) {
    var party_type = frm.doc[partyTypeField];
    var party_name_label = "";
    if (party_type === 'Employee') {
        party_name_label = "Employee Name";
    } else if (party_type === 'Faculty Member') {
        party_name_label = "Faculty Member Name";
    } else if (party_type === 'Student') {
        party_name_label = "Student Name";
    } else {
        party_name_label = "Party Name";
    }

    frm.set_df_property(partyNameField, 'label', party_name_label);
    frm.refresh_field(partyNameField);
}


function fetch_party_name(frm, partyType, partyField, partyNameField, employeeFieldName, facultyMemberFieldName, studentFieldName) {
    if (frm.doc[partyField]) {
        var fieldname = '';
        switch (partyType) {
            case 'Employee':
                fieldname = employeeFieldName;
                break;
            case 'Faculty Member':
                fieldname = facultyMemberFieldName;
                break;
            case 'Student':
                fieldname = studentFieldName;
                break;
        }

        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: partyType,
                fieldname: fieldname,
                filters: { 'name': frm.doc[partyField] }
            },
            callback: function (r) {
                if (r.message && r.message[fieldname]) {
                    frm.set_value(partyNameField, r.message[fieldname]);
                } else {
                    frm.set_value(partyNameField, 'None');
                }
            }
        });
    } else {
        frm.set_value(partyNameField, '');
    }
}

function clear_evaluatee_information(frm) {
    if (frm.doc.company) {
        frm.set_value('company', '');
    }
    if (frm.doc.department) {
        frm.set_value('department', '');
    }
    if (frm.doc.faculty) {
        frm.set_value('faculty', '');
    }
    if (frm.doc.email) {
        frm.set_value('email', '');
    }
    if (frm.doc.designation) {
        frm.set_value('designation', '');
    }
    if (frm.doc.academic_rank) {
        frm.set_value('academic_rank', '');
    }
}


function fetch_evaluatee_information(frm, partyType, partyName) {
    var fields_to_fetch = [];

    if (partyType === 'Employee') {
        fields_to_fetch = ['user_id', 'designation', 'company', 'department'];
    } else if (partyType === 'Faculty Member') {
        fields_to_fetch = ['email', 'academic_rank', 'faculty', 'company', 'department'];
    }

    fields_to_fetch.forEach(function (field) {
        var target_field = field === 'user_id' ? 'email' : field;
        frm.set_value(target_field, '');
    });

    frappe.call({
        method: 'frappe.client.get',
        args: {
            doctype: partyType,
            name: partyName
        },
        callback: function (r) {
            if (r.message) {
                fields_to_fetch.forEach(function (field) {
                    var target_field = field === 'user_id' ? 'email' : field;
                    frm.set_value(target_field, r.message[field] || '');
                });
            }
        }
    });
}