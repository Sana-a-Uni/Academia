// Copyright (c) 2023, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Faculty Member", {
    refresh: function(frm) {
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

    onload: function(frm) {
        frm.events.filtering_faculty(frm);
        frm.events.filtering_department(frm);
    },

    validate: function(frm) {
        frm.events.validate_extension(frm);
        frm.events.validate_child_extension(frm, 'faculty_member_academic_ranking', 'attachment', "Attachment File");
        frm.events.validate_child_extension(frm, 'faculty_member_training_course', 'certification', "Certification File");
        frm.events.validate_date(frm);
        frm.events.validate_current_academic_rank(frm);
    },

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

        const validate_single_date = function(row, table_name) {
            if (row.date && row.date > today) {
                frappe.throw(__('Date in {0} table cannot be in the future.', [table_name]));
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

    company: function(frm) {
        if (frm.doc.faculty) {
            frm.set_value('faculty', '');
        }
        frm.events.filtering_faculty(frm);
        frm.events.filtering_department(frm);
    },

    filtering_faculty: function(frm) {
        frm.set_query("faculty", function() {
            return {
                filters: {
                    "company": frm.doc.company
                }
            };
        });
    },

    filtering_department: function(frm) {
        frm.set_query("department", function() {
            return {
                filters: {
                    "company": frm.doc.company
                }
            };
        });
    },

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
        if (frm.doc.faculty_member_academic_ranking && frm.doc.faculty_member_academic_ranking.length > 0) {
            var rank_list = frm.doc.faculty_member_academic_ranking.map(function(row) {
                return row.academic_ranking;
            });

            rank_list.sort((a, b) => a - b);

            var latest_academic_rank = rank_list[rank_list.length - 1];
            frm.set_value('academic_rank', latest_academic_rank);
            frm.refresh_field('academic_rank');
        } else {
            console.log('Faculty Member Academic Ranking table is empty.');
        }
    }
});

frappe.ui.form.on('Faculty Member Academic Ranking', {
    faculty_member_academic_ranking_add: function (frm) {
        frm.fields_dict['faculty_member_academic_ranking'].grid.get_field('academic_ranking').get_query = function (doc) {
            let rank_list = [];

            if (!doc.__islocal && doc.academic_ranking) {
                rank_list.push(doc.academic_ranking);
            }

            frm.doc.faculty_member_academic_ranking.forEach(function(row) {
                if (row.academic_ranking) {
                    rank_list.push(row.academic_ranking);
                }
            });

            rank_list = [...new Set(rank_list)];

            return {
                filters: [['Academic Rank', 'name', 'not in', rank_list]]
            };
        };
    }
});
