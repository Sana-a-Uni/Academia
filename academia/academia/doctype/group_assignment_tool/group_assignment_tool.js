// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on('Group Assignment Tool', {
    "get_courses": function(frm) {
		frm.set_value("courses",[]);
		frappe.call({
			method: "get_courses",
			doc:frm.doc,
			callback: function(r) {
				if(r.message) {
					frm.set_value("courses", r.message);
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
        }),
        frm.set_query('program', function() {
            if (frm.doc.faculty) {
                return {
                    filters: {
                        'faculty': frm.doc.faculty
                    }
                };
            } else {
                return {};
            }
        }),
        frm.set_query('student_batch', function() {
            if (frm.doc.program) {
                return {
                    filters: {
                        'program_specification': frm.doc.program
                    }
                };
            } else {
                return {};
            }
        }),
        frm.set_query('group', function() {
            if (frm.doc.student_batch) {
                return {
                    filters: {
                        'batch': frm.doc.student_batch
                    }
                };
            } else {
                return {};
            }
        });
    },
    faculty: function(frm) {
        frm.set_value('program', null);  // Reset the program field when faculty changes
        frm.set_query('program', function() {
            if (frm.doc.faculty) {
                return {
                    filters: {
                        'faculty': frm.doc.faculty
                    }
                };
            } else {
                return {};
            }
        });
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
    },
    program: function(frm) {
		frm.set_value('student_batch', null);
		frm.set_query('student_batch', function() {
            if (frm.doc.program) {
                return {
                    filters: {
                        'program_specification': frm.doc.program
                    }
                };
            } else {
                return {};
            }
        });
    },
    student_batch: function(frm) {
		frm.set_value('group', null);
		frm.set_query('group', function() {
            if (frm.doc.student_batch) {
                return {
                    filters: {
                        'batch': frm.doc.student_batch
                    }
                };
            } else {
                return {};
            }
        });
    }
});
