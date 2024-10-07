// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

var cancelled_compensatory_lessons_js 
frappe.ui.form.on("Lesson Scheduling Tool", {
	refresh(frm) {
        frm.disable_save();
		frm.fields_dict.lesson_start_date.datepicker.update({ 
            minDate: new Date(frappe.datetime.get_today()),
        });		
		frm.trigger("load_filters");
		frm.page.set_primary_action(__('Schedule Lesson'), () => {
			frappe.dom.freeze(__("Scheduling..."));
			frm.call('schedule_lesson')
				.fail(() => {
					frappe.dom.unfreeze();
					frappe.msgprint(__("Lesson Scheduling Failed"));
				})
				.then(r => {
					frappe.dom.unfreeze();
					if (!r.message) {
						frappe.throw(__('There were errors creating Course Schedule'));
					}
					const { course_schedules } = r.message;
					if (r.message["course_schedules"].length > 0) {
						unhide_field("scheduled_lessons_section");
						unhide_field("scheduled_lesson_html");
						frm.events.show_scheduled_lessons(frm, r.message["course_schedules"], r.message["groups"])
					} else {
						hide_field("scheduled_lesson_html");
					}
					if (r.message["cancelled_comcompensatory_lessons"].length > 0) {
						unhide_field("cancelled_compensatory_lessons_section");
						unhide_field("cancelled_compensatory_lesson_html");
						cancelled_compensatory_lessons_js = r.message["cancelled_comcompensatory_lessons"];
						const {cancelled_comcompensatory_lessons} = r.message;
						frappe.msgprint({
							title: __('Notification'),
							indicator: 'green',
							message: __(cancelled_comcompensatory_lessons.length + " Cancelled Compensatory Lesson")
						});

						const cancelled_comcompensatory_lessons_html = cancelled_comcompensatory_lessons.map(c =>`	
							<tr>
								<td><a href="/app/compensatory-lesson/${c.name}">${c.name}</a></td>
								<td>${c.instructor_name}</td>
								<td>${c.date}</td>
							</tr>
						`).join('');

						const html = `
							<table class="table table-bordered">
								<thead><tr><th>${__("Compensatory Lesson")}</th><th>${__("Instructor")}</th><th>${__("Date")}</th></tr></thead>
								<tbody>
									${cancelled_comcompensatory_lessons_html}
								</tbody>
							</table>
						`;

						frm.set_df_property("cancelled_compensatory_lesson_html", "options", html);
						
					} else {
						hide_field("cancelled_compensatory_lessons_section");
					}

					if (course_schedules) {						
						frappe.msgprint({
							title: __('Notification'),
							indicator: 'green',
							message: __(course_schedules.length + " Lesson created")
						});
					}
				});
		});
	},

	schedule_template_version(frm) {
		frm.trigger("load_filters");
	},

	academic_program(frm) {
		frm.trigger("load_filters");
		if (frm.doc.academic_program == "All Programs") {
			frm.set_value("specific_program", "");
		}	
	},

	specific_program(frm) {
		frm.trigger("load_filters");
	},

	level(frm) {
		frm.trigger("load_filters");
		if (frm.doc.level == "All Levels") {
			frm.set_value("specific_level", "");
		}
		if(level.df.onchange) {
			level.df.onchange = function() {
				frappe.msgprint("on change")
			};
		}
	},

	specific_level(frm) {
		frm.trigger("load_filters");
		
	},

	lesson_start_date(frm) {
		if(frm.doc.lesson_start_date) {
			frm.fields_dict.lesson_end_date.datepicker.update({ 
				minDate: new Date(frm.doc.lesson_start_date),
			});
		}
		
	},

	load_filters(frm) {
		frm.call('get_filters_data')
		.then(r => {
			if (r.message) {
				let programs = r.message['programs'];
				let levels = r.message['levels'];
				let groups = r.message['groups'];
				
				frm.set_query("specific_program", function(){
					return {
						"filters": [
							['name', 'in', programs]
						]                    
					}
				})
				frm.set_query("specific_level", function(){
					return {
						"filters": [
							['name', 'in', levels]
						]                    
					}
				})
				frm.set_query("group", function(){
					return {
						"filters": [
							['student_group_name', 'in', groups]
						]                    
					}
				})
			}
        })
	},

	show_scheduled_lessons(frm, course_schedules, groups) {
		const $wrapper = frm.get_field("scheduled_lesson_html").$wrapper;
		const summary_wrapper = $(`<div class="summary_wrapper">`).appendTo($wrapper);
		const data = course_schedules.map((entry) => {
			group = "";
			if(entry.is_multi_group == 1) {
				for (let i = 0; i < groups.length; i++) {
						if(entry.name == groups[i].parent){
							for (let j = 0; j < groups[i].values.length; j++) {
								if(j + 1 < groups[i].values.length){
									group += groups[i].values[j] + "&";
								} else {
									group += groups[i].values[j];
								}
								
							}
							return [entry.name ,entry.instructor_name ,entry.course ,group, entry.date,`${entry.from_time} : ${entry.to_time}`];
						}
					  }
			}
			return [entry.name ,entry.instructor_name ,entry.course ,entry.group, entry.date,`${entry.from_time} : ${entry.to_time}`];
		});

		frm.events.render_datatable(frm, data, summary_wrapper);
	},

	render_datatable(frm, data, summary_wrapper) {
		const columns = frm.events.get_columns_for_scheduled_lesson_table(frm);

		if (!frm.scheduled_lesson_datatable) {
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
			frm.scheduled_lesson_datatable = new frappe.DataTable(
				summary_wrapper.get(0),
				datatable_options,
			);
		} else {
			frm.scheduled_lesson_datatable.refresh(data, columns);
		}
	},

	get_columns_for_scheduled_lesson_table(frm) {
		return [
			{
				name: "id",
				id: "id",
				content: __("ID"),	
				editable: false,
				sortable: false,
				focusable: false,
				dropdown: false,
				align: "left",
				width: 100,
				format: (value) => {
					return `<a href='/app/lesson/${__(value)}'>${__(value)}</a>`
				}
			},
			{
				name: "instructor",
				id: "instructor",
				content: __("Instructor"),
				editable: false,
				sortable: false,
				focusable: false,
				dropdown: false,
				align: "left",
				width: 170,
			},
			{
				name: "course",
				id: "course",
				content: __("Course"),	
				editable: false,
				sortable: false,
				focusable: false,
				dropdown: false,
				align: "left",
				width: 180,
			},
			{
				name: "group",
				id: "group",
				content: __("Group"),	
				editable: false,
				sortable: false,
				focusable: false,
				dropdown: false,
				align: "left",
				width: 180,
			},
			{
				name: "date",
				id: "date",
				content: __("Date"),	
				editable: false,
				sortable: false,
				focusable: false,
				dropdown: false,
				align: "left",
				width: 120,
			},
			{
				name: "time",
				id: "time",
				content: __("Time"),	
				editable: false,
				sortable: false,
				focusable: false,
				dropdown: false,
				align: "left",
				width: 160,
			}
		]
	},

	"export_to_pdf": function(frm) {
		frappe.prompt([
			{'fieldname': 'file_name', 'fieldtype': 'Data', 'label': 'File Name', 'reqd': 1}
		],
		function(values){
			const cancelled_compensatory_lessons = cancelled_compensatory_lessons_js;
			download_pdf(cancelled_compensatory_lessons, values.file_name);
		},
		'Enter File Name',
		'Generate PDF'
		);
		function download_pdf(cancelled_compensatory_lessons, file_name) {
			try {
				const encodedLessons = encodeURIComponent(JSON.stringify(cancelled_compensatory_lessons));
				const url = frappe.urllib.get_full_url(
					`/api/method/academia.academic_attendance.doctype.lesson_scheduling_tool.lesson_scheduling_tool.generate_pdf?cancelled_compensatory_lessons=${encodedLessons}&file_name=${file_name}`
				);
		
				console.log(`Initiating download for: ${url}`);
		
				fetch(url)
					.then(response => {
						if (!response.ok) {
							console.error(`HTTP error! status: ${response.status}`);
							throw new Error(`HTTP error! status: ${response.status}`);
						}
						return response.blob();
					})
					.then(blob => {
						const a = document.createElement('a');
						const url = window.URL.createObjectURL(blob);
						a.href = url;
						a.download = `${file_name}.pdf`;
						document.body.appendChild(a);
						a.click();
						setTimeout(() => {
							document.body.removeChild(a);
							window.URL.revokeObjectURL(url);
						}, 0);
					})
					.catch(error => {
						console.error('Error downloading PDF:', error);
						frappe.msgprint(__('An error occurred while downloading the PDF.'));
					});
			} catch (error) {
				console.error('Error forming the request URL:', error);
				frappe.msgprint(__('An error occurred while forming the request URL.'));
			}
		}
		
	},
});