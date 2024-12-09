// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Program Enrollment Tool", {
	refresh(frm) {
		frm.set_query("academic_term", function () {
			if (frm.doc.academic_year) {
				return {
					filters: {
						academic_year: frm.doc.academic_year,
					},
				};
			} else {
				return {};
			}
		});
	},

	get_student: function (frm) {
		new frappe.ui.form.MultiSelectDialog({
			doctype: "Student",
			target: frm,
			setters: {
				student_name: null,
				first_name: frm.doc.first_name,
				gender: frm.doc.gender,
				// designation: null,
			},
			// add_filters_group: 1,
			// date_field: "transaction_date",
			get_query() {
				return {
					filters: { docstatus: ["!=", 2] },
				};
			},
			primary_action_label: __("Get Student"),

			action(selections) {
				// console.log(d.dialog.get_value("company"));
				// emptying Council members
				frm.set_value("students", []);
				// Hold employee names
				selections.forEach((student, index, array) => {
					frappe.db.get_value(
						"Student",
						student,
						["name", "student_name", "first_name", "gender"],
						(student) => {
							if (student) {
								frm.add_child("students", {
									student_id: student.name,
									student_name: student.student_name,
									first_name: student.first_name,
									gender: student.gender,
								});
								// Refreshing the Council Members in the last itration
								console.log(`array => ${array}`);
								if (index === array.length - 1) {
									frm.refresh_field("students");
								}
							}
						}
					);
				});
				this.dialog.hide();
			},
		});
	},

	clear_students: function (frm) {
		frm.clear_table("students");
		frm.refresh_field("students");
	},

	refresh: function (frm) {
		frm.disable_save();
		frm.add_custom_button(__("Enroll Students"), function () {
			frappe.call({
				method: "academia.academia.doctype.program_enrollment_tool.program_enrollment_tool.enroll_students", // Adjust path accordingly
				args: {
					doc: frm.doc,
				},
				callback: function (r) {
					if (!r.exc) {
						frappe.msgprint(__("Students enrolled successfully."));
					} else {
						frappe.msgprint(__("There was an error enrolling students."));
					}
				},
			});
		});
	},
});
