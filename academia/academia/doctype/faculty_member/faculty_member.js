// Copyright (c) 2023, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Faculty Member", {
    // Start of refresh event
    refresh: function(frm) {
        // Refresh fetched field 'employment_type'
        frappe.db.get_value("Employee", frm.doc.employee, "employment_type", function(value) {
            if (value && value.employment_type) {
                frm.set_value('employment_type', value.employment_type);
            }
            frm.refresh_field('employment_type');
        });

        frappe.db.get_value("Employee", frm.doc.employee, "department", function(value) {
            if (value && value.department) {
                frm.set_value('department', value.department);
            }
            frm.refresh_field('department');
        });
    },
    // End of refresh event

    // Start of onload event
    onload: function(frm) {
        // Calling functions
        frm.events.filtering_faculty(frm);
        frm.events.filtering_department(frm);
    },
    // End of onload event

    // Start of validate event
    validate: function(frm) {
        // Calling functions
        frm.events.validate_extension(frm);
        frm.events.validate_child_extension(frm, 'faculty_member_academic_ranking', 'attachment', "Attachment File");
        frm.events.validate_child_extension(frm, 'faculty_member_training_course', 'certification', "Certification File");
        frm.events.validate_date(frm);
        frm.events.validate_current_academic_rank(frm);
    },
    // End of validate event

    // FN: validate 'decision_attachment' extensions
    validate_extension: function(frm) {
        var decision_attachment = frm.doc.decision_attachment;
        if (decision_attachment) {
            var allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg'];
            var decision_attachment_extension = '.' + decision_attachment.split('.').pop().toLowerCase();
            if (!allowed_extensions.includes(decision_attachment_extension)) {
                frappe.throw(__("Decision File has an invalid extension. Only files with extensions {0} are allowed.", [allowed_extensions.join(', ')]));
                frappe.validated = false;
            }
        }
    },

    // FN: validate file extensions of child tables
    validate_child_extension: function(frm, child_table_name, attachment_field_name, error_message) {
        if (frm.doc[child_table_name]) {
            frm.doc[child_table_name].forEach(function(row) {
                if (row[attachment_field_name]) {
                    var allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg'];
                    var attachment_extension = '.' + row[attachment_field_name].split('.').pop().toLowerCase();
                    if (!allowed_extensions.includes(attachment_extension)) {
                        frappe.throw(__(error_message + ' ' + row[attachment_field_name] + " has an invalid extension. Only files with extensions " + allowed_extensions.join(', ') + " are allowed."));
                        frappe.validated = false;
                    }
                }
            });
        }
    },

    // FN: validate dates of child tables
    validate_date: function(frm) {
        const today = frappe.datetime.get_today();

        const validate_date_range = function(row, table_name) {
            if (row.starts_on && row.starts_on > today) {
                frappe.throw(__('Start date in {0} table cannot be in the future.', [table_name]));
            }
            if (row.ends_on && row.ends_on > today) {
                frappe.throw(__('End date in {0} table cannot be in the future.', [table_name]));
            }
            if (row.starts_on && row.ends_on && row.ends_on < row.starts_on) {
                frappe.throw(__('End date in {0} table must be after the start date.', [table_name]));
            }
        };

        if (frm.doc['faculty_member_training_course']) {
            frm.doc['faculty_member_training_course'].forEach(function(row) {
                validate_date_range(row, 'training courses');
            });
        }

        if (frm.doc['faculty_member_conference_and_workshop']) {
            frm.doc['faculty_member_conference_and_workshop'].forEach(function(row) {
                validate_date_range(row, 'conferences and workshops');
            });
        }

        const validate_single_date = function(row, table_name) {
            if (row.date && row.date > today) {
                frappe.throw(__('Date in {0} table cannot be in the future.', [table_name]));
            }
        };

        if (frm.doc['faculty_member_university_and_community_service']) {
            frm.doc['faculty_member_university_and_community_service'].forEach(function(row) {
                validate_single_date(row, 'university and community services');
            });
        }

        if (frm.doc['faculty_member_activity']) {
            frm.doc['faculty_member_activity'].forEach(function(row) {
                validate_single_date(row, 'activities');
            });
        }

        if (frm.doc['faculty_member_award_and_appreciation_certificate']) {
            frm.doc['faculty_member_award_and_appreciation_certificate'].forEach(function(row) {
                validate_single_date(row, 'awards and appreciation certificates');
            });
        }
    },

    // FN: Clearing faculty and department fields when value of company changes
    company: function(frm) {
        if (frm.doc.faculty) {
            frm.set_value('faculty', '');
        }
        // Calling functions
        frm.events.filtering_faculty(frm);
        frm.events.filtering_department(frm);
    },

    // FN: Filtering faculty field by company field
    filtering_faculty: function(frm) {
        frm.set_query("faculty", function() {
            return {
                filters: {
                    "company": frm.doc.company
                }
            };
        });
    },

    // FN: Filtering department field by company field
    filtering_department: function(frm) {
        frm.set_query("department", function() {
            return {
                filters: {
                    "company": frm.doc.company
                }
            };
        });
    },

    // FN: Handle 'from_another_university' field
    from_another_university: function(frm) {
        let selected_university = frm.doc.from_another_university;

        frm.set_query('external_faculty', function() {
            return {
                filters: {
                    university: selected_university
                }
            };
        });

        frm.set_value('external_faculty', null);
    },

    validate_current_academic_rank: function (frm) {
        var rank_list = [];
        frm.doc.faculty_member_academic_ranking.forEach(function (row) {
            rank_list.push(row.academic_rank);
        });
        if (rank_list.length > 0) {
            rank_list.sort((a, b) => a - b);
            var latest_academic_rank = rank_list[rank_list.length - 1];
            frm.set_value('current_academic_rank', latest_academic_rank);
            frm.refresh_field('current_academic_rank');
        } else {
            console.log('Faculty Member Academic Ranking table is empty.');
        }
    },

});

// --- Start of 'Faculty Member Academic Ranking' childe table form scripts ---
frappe.ui.form.on('Faculty Member Academic Ranking', {
    // FN: filter duplicate 'academic_rank' field in 'faculty_member_academic_ranking' child table
    faculty_member_academic_ranking_add: function (frm) {
        frm.fields_dict['faculty_member_academic_ranking'].grid.get_field('academic_rank').get_query = function (doc) {
            let rank_list = [];
            if (!doc.__islocal) rank_list.push(doc.academic_rank);
            $.each(doc.faculty_member_academic_ranking, function (idx, val) {
                if (val.academic_rank) rank_list.push(val.academic_rank);
            });
            return { filters: [['Academic Rank', 'name', 'not in', rank_list]] };
        };
    },
    // End of the function

});
// End of childe table form scripts