// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on('Student Group Tool', {
    "get_students": function(frm) {
        frm.set_value("students",[]);
		frappe.call({
			method: "get_students",
			doc:frm.doc,
			callback: function(r) {
				if(r.message) {
					frm.set_value("students", r.message);
				}
			}
		});
	},
	"generate_groups": function(frm) {
		//frm.set_value("courses",[]);
		frappe.call({
			method: "generate_groups_ultra",
			doc:frm.doc,
			callback: function(r) {
				if(r.message) {
					//frm.set_value("courses", r.message);
				}
			}
		});
	},
	onload: function(frm) {
 	
		const urlParams = new URLSearchParams(window.location.search);
		//const based_on = urlParams.get('based_on');
		//const capacity = urlParams.get('capacity');
	   const student_group = urlParams.get('student_group');
	   const based_on = urlParams.get('based_on');
	   const grouping_by = urlParams.get('grouping_by')
		
		 if (based_on) {
			 frm.set_value('based_on', based_on);
		 }
		// if (capacity) {
		// 	frm.set_value('capacity', capacity);
		// }
		if (student_group) {
		   frm.set_value('student_group', student_group);
	   }
		if (grouping_by) {
		   frm.set_value('grouping_by', grouping_by);
	   }
		
	},
	refresh: function(frm) {
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
		frm.set_query('student_group', function() {
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
        frm.set_value('program', null);
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
		frm.set_value('student_group', null);
		frm.set_query('student_group', function() {
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

