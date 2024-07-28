// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Academic Attendance Tool", {
	refresh(frm) {
		frm.trigger("reset_attendance_fields")
		frm.trigger("load_faculty_members");
		frm.trigger("set_primary_action");

		frm.add_custom_button('Lesson Attendance List', () => {
            frappe.set_route('List','Lesson Attendance','List')
        })
	},

	onload(frm) {
		frm.set_value("date", frappe.datetime.get_today());
        frm.set_value("from_time", "");
        frm.set_value("to_time", "");
	},

	date(frm) {
		frm.trigger("load_faculty_members");
	},

    from_time(frm) {
		frm.trigger("load_faculty_members");
	},

    to_time(frm) {
		frm.trigger("load_faculty_members");
	},

	faculty(frm) {
		frm.trigger("load_faculty_members");

		frm.set_query("program", function(){
			return {
				"filters": {
					"faculty": frm.doc.faculty
				}
			}
		})

		frm.set_query("building", function(){
			return {
				"filters": {
					"faculty": frm.doc.faculty
				}
			}
				
		})

		frm.set_query("room", function(){
			return {
				"filters": {
					"faculty": frm.doc.faculty
				}
			}
		})
	},

	room(frm) {
		frm.trigger("load_faculty_members");
	},

	program(frm) {
		frm.trigger("load_faculty_members");
	},

	building(frm) {
		frm.set_query("room", function(){
			return {
				"filters": {
					"building": frm.doc.building
				}
			}
		})

		if (!frm.doc.building && frm.doc.faculty) {
			frm.set_query("room", function(){
				return {
					"filters": {
						"faculty": frm.doc.faculty
					}
				}
			})
		}
	},

	status(frm) {
		frm.trigger("set_primary_action");
	},

	reset_attendance_fields(frm) {
		frm.set_value("status", "");
		frm.set_value("late_entry", 0);
        frm.set_value("late_entry_time", "");
        frm.set_value("note", "");
	},

	load_faculty_members(frm) {
		if (!frm.doc.date)
			return;

		frappe.call({
			method: "academia.academic_attendance.doctype.academic_attendance_tool.academic_attendance_tool.get_employees",
			args: {
				date: frm.doc.date,
                from_time: frm.doc.from_time,
                to_time: frm.doc.to_time,
				faculty: frm.doc.faculty,
                academic_program: frm.doc.program,
                room: frm.doc.room
			}
		}).then((r) => {
			frm.employees = r.message["unmarked"];

			if (r.message["unmarked"].length > 0) {
				unhide_field("unmarked_attendance_section");
				unhide_field("attendance_details_section");
				frm.events.show_unmarked_employees(frm, r.message["unmarked"]);
			} else {
				hide_field("unmarked_attendance_section");
				hide_field("attendance_details_section");
			}

			if (r.message["marked"].length > 0) {
				unhide_field("marked_attendance_html");
				frm.events.show_marked_employees(frm, r.message["marked"]);
			} else {
				hide_field("marked_attendance_html");
			}
		});
	},

	show_unmarked_employees(frm, unmarked_employees) {
		const $wrapper = frm.get_field("employees_html").$wrapper;
		$wrapper.empty();
		const employee_wrapper = $(`<div class="employee_wrapper">`).appendTo($wrapper);
		function number_of_columns(){
			if(window.innerWidth <= 1920 && window.innerWidth >= 1025)
				return 4;
			else if(window.innerWidth <= 1224 && window.innerWidth >= 1051)
				return 3;
			else if(window.innerWidth <= 1050 && window.innerWidth >= 780)
				return 2;
			else
				return 1;
		}
		
		function lesson_info(employee){
			if(employee.is_multi_group){
				let info = employee.multi_info;
				let text ="";
				for(let i = 0; i < info.length; i++){
					text += info[i]["program"] + " " + info[i]["level"] + " " + info[i]["group"] + "</br>";
				}
				return text;
			}
			if(employee.course_type === "Practical"){

				return employee.level + '-' + employee.program + employee.group + '-' + employee.sub_group;
			}	
			 return employee.level + '-' + employee.program + employee.group;
		}

		frm.employees_multicheck = frappe.ui.form.make_control({
			parent: employee_wrapper,
			df: {
				fieldname: "employees_multicheck",
				fieldtype: "MultiCheck",
				select_all: true,
				columns: number_of_columns(),
				get_data: () => {
					return unmarked_employees.map((lesson) => {
						return {
							label: `<div class="card text-white mb-3" style="max-width: 18rem;text-align:center">
										<div class="card-header" dir="rtl" style="text-align:center">${lesson.faculty_member_name} - ${lesson.name}</div>
										<div class="card-body">
											<h5 class="card-title" id="info">${lesson_info(lesson)}</h5>
											<p class="card-text" style="color:black">${lesson.course} 
												</br> ${lesson.room} 
												</br> Time : ${lesson.from_time} - ${lesson.to_time}
											</p>
										</div>
									</div>`,
							value: lesson.name,
							checked: 0,
						};
					});
				},
			},
			render_input: true,
		});

		frm.employees_multicheck.refresh_input();
	},

	show_marked_employees(frm, marked_employees) {
		const $wrapper = frm.get_field("marked_attendance_html").$wrapper;
		const summary_wrapper = $(`<div class="summary_wrapper">`).appendTo($wrapper);

		const data = marked_employees.map((entry) => {
			return [`${entry.faculty_member} : ${entry.faculty_member_name}`, entry.status];
		});

		frm.events.render_datatable(frm, data, summary_wrapper);
	},

	render_datatable(frm, data, summary_wrapper) {
		const columns = frm.events.get_columns_for_marked_attendance_table(frm);

		if (!frm.marked_emp_datatable) {
			const datatable_options = {
				columns: columns,
				data: data,
				dynamicRowHeight: true,
				inlineFilters: true,
				layout: "fixed",
				cellHeight: 35,
				noDataMessage: __("No Data"),
				disableReorderColumn: true,
			};
			frm.marked_emp_datatable = new frappe.DataTable(
				summary_wrapper.get(0),
				datatable_options,
			);
		} else {
			frm.marked_emp_datatable.refresh(data, columns);
		}
	},

	get_columns_for_marked_attendance_table(frm) {
		return [
			{
				name: "employee",
				id: "employee",
				content: __("Employee"),
				editable: false,
				sortable: false,
				focusable: false,
				dropdown: false,
				align: "left",
				width: 350,
			},
			{
				name: "status",
				id: "status",
				content: __("Status"),
				editable: false,
				sortable: false,
				focusable: false,
				dropdown: false,
				align: "left",
				width: 150,
				format: (value) => {
					if (value == "Present" || value == "Work From Home")
						return `<span style="color:green">${__(value)}</span>`;
					else if (value == "Absent")
						return `<span style="color:red">${__(value)}</span>`;
					else if (value == "Half Day")
						return `<span style="color:orange">${__(value)}</span>`;
					else if (value == "Leave")
						return `<span style="color:#318AD8">${__(value)}</span>`;
				}
			},
		]
	},

	set_primary_action(frm) {
		frm.disable_save();
		frm.page.set_primary_action(__("Mark Attendance"), () => {
			if (frm.employees.length === 0) {
				frappe.msgprint({
					message: __("Attendance for all the employees under this criteria has been marked already."),
					title: __("Attendance Marked"),
					indicator: "green"
				});
				return;
			}

			if (frm.employees_multicheck.get_checked_options().length === 0) {
				frappe.throw({
					message: __("Please select the faculty member you want to mark attendance for."),
					title: __("Mandatory")
				});
			}

			if (!frm.doc.status) {
				frappe.throw({
					message: __("Please select the attendance status."),
					title: __("Mandatory")
				});
			}

			if (!frm.doc.late_entry) {
				frm.doc.late_entry_time = ""
			}

			frm.trigger("mark_attendance");
		});
	},

	mark_attendance(frm) {
		const marked_employees = frm.employees_multicheck.get_checked_options();

		frappe.call({
			method: "academia.academic_attendance.doctype.academic_attendance_tool.academic_attendance_tool.mark_employee_attendance",
			args: {
				employee_list: marked_employees,
				status: frm.doc.status,
				date: frm.doc.date,
				late_entry: frm.doc.late_entry,
				late_entry_time : frm.doc.late_entry_time,	
				note: frm.doc.note,
			},
			freeze: true,
			freeze_message: __("Marking Attendance")
		}).then((r) => {
			if (!r.exc) {
				frappe.show_alert({ message: __("Attendance marked successfully"), indicator: "green" });
				frm.refresh();
			}
		});
	},
});