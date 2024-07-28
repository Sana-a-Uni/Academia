// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on('Course Enrollment Tool', {
    "get_courses": function(frm) {
		frm.set_value("courses",[]);
        frm.set_value("students",[]);
		frappe.call({
			method: "get_courses",
			doc:frm.doc,
			callback: function(r) {
				if(r.message) {
					frm.set_value("courses", r.message.courses);
                    frm.set_value("students", r.message.students);
				}
			}
		});
	},
	"generate": function(frm) {
		//frm.set_value("courses",[]);
		frappe.call({
			method: "generate",
			doc:frm.doc,
			callback: function(r) {
				if(r.message) {
					//frm.set_value("courses", r.message);
				}
			}
		});
	},
	refresh: function(frm) {
        // Add filter for Specific Program based on Faculty
        frm.fields_dict['specific_program'].get_query = function(doc) {
            return {
                filters: {
                    'faculty': doc.faculty
                }
            };
        };
        frm.set_query('academic_term', function() {
            if (frm.doc.academic_year) {
                return {
                    filters: {
                        'academic_year': frm.doc.academic_year
                    }
                };
            } else {
                return {};
            }
        });
    },
    faculty: function(frm) {
        // Clear Specific Program field when Faculty is changed
        frm.set_value('specific_program', null);

        // Trigger the filter update for Specific Program
        frm.fields_dict['specific_program'].get_query = function(doc) {
            return {
                filters: {
                    'faculty': doc.faculty
                }
            };
        };
    },
    academic_year: function(frm) {
        frm.set_value('academic_term', null);
        frm.set_query('academic_term', function() {
            if (frm.doc.academic_year) {
                return {
                    filters: {
                        'academic_year': frm.doc.academic_year
                    }
                };
            } else {
                return {};
            }
        });
    }
});
