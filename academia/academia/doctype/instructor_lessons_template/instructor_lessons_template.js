// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Instructor Lessons Template", {
	refresh: function (frm) {
		// Ensure all required fields are selected before calling the API
		if (frm.doc.schedule_type && frm.doc.faculty && frm.doc.schedule_template_version) {
			let identifier = null;

			// Handle different schedule types
			if (["Instructor", "Group", "Room"].includes(frm.doc.schedule_type)) {
				if (frm.doc.schedule_type === "Instructor" && frm.doc.instructor) {
					identifier = frm.doc.instructor;
				} else if (frm.doc.schedule_type === "Group" && frm.doc.group) {
					identifier = frm.doc.group;
				} else if (frm.doc.schedule_type === "Room" && frm.doc.room) {
					identifier = frm.doc.room;
				} else {
					frm.fields_dict.lessons.$wrapper.html(
						'<div style="text-align: center;">Please select the required field for the chosen schedule type.</div>'
					);
					return;
				}
			}

			// Call the API to fetch the lessons data
			frappe.call({
				method: "academia.academia.doctype.instructor_lessons_template.instructor_lessons_template.get_lessons_data",
				args: {
					schedule_type: frm.doc.schedule_type,
					identifier: identifier,
					faculty: frm.doc.faculty,
					schedule_template_version: frm.doc.schedule_template_version,
				},
				callback: function (r) {
					if (r.message) {
						const lessons = r.message;
						let tableHTML = "";

						// Loop through the grouped lessons and generate the tables
						Object.keys(lessons).forEach((key) => {
							tableHTML += `
                                <div style="text-align: center; margin-bottom: 15px;">
                                    <h3> Semester schedule ${frm.doc.academic_term} for the academic year ${frm.doc.academic_year}</h3>
                                    <p> - ${frm.doc.faculty} - ${frm.doc.schedule_template_version}</p>
                                    <p> - ${frm.doc.schedule_type}: ${key}</p>
                                </div>
                                <div>
                                    <h4>${key}</h4>
                                    <table border="1" style="width: 100%; text-align: center; border-collapse: collapse;">
                                        <tr>
                                            <th></th>
                                            <th>1 <br>08:00 - 10:00</th>
                                            <th>2 <br>10:00 - 12:00</th>
                                            <th>3 <br>12:00 - 14:00</th>
                                            <th>4 <br>14:00 - 16:00</th>
                                            <th>5 <br>16:00 - 18:00</th>
                                        </tr>
                            `;

							Object.keys(lessons[key]).forEach((day) => {
								tableHTML += `<tr><th>${day}</th>`;
								lessons[key][day].forEach((slot) => {
									tableHTML += slot
										? `<td style="height: 100px;">
                                            <div>${slot.group || ""}</div>
                                            <div>${slot.course || ""}</div>
                                            <div>${slot.instructor || ""}</div>
                                            <div>${slot.room || ""}</div>
                                           </td>`
										: `<td style="height: 100px;"></td>`;
								});
								tableHTML += `</tr>`;
							});

							tableHTML += `</table></div>`;
						});

						// Display the generated HTML
						frm.fields_dict.lessons.$wrapper.html(tableHTML);
					} else {
						frm.fields_dict.lessons.$wrapper.html(
							'<div style="text-align: center;">No lessons found for the selected criteria.</div>'
						);
					}
				},
				error: function () {
					frm.fields_dict.lessons.$wrapper.html(
						'<div style="text-align: center; color: red;">An error occurred while fetching the lessons.</div>'
					);
				},
			});
		} else {
			frm.fields_dict.lessons.$wrapper.html(
				'<div style="text-align: center;">Please select the necessary fields (Schedule Type, Faculty, and Schedule Template Version).</div>'
			);
		}
	},

	// Trigger the refresh on changes in relevant fields
	schedule_type: function (frm) {
		frm.trigger("refresh");
	},

	instructor: function (frm) {
		frm.trigger("refresh");
	},

	faculty: function (frm) {
		frm.trigger("refresh");
	},

	schedule_template_version: function (frm) {
		frm.trigger("refresh");
	},

	group: function (frm) {
		frm.trigger("refresh");
	},

	room: function (frm) {
		frm.trigger("refresh");
	},
});
