// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Study Plan Course", {
	table_ytno_add: function (frm) {
		frm.fields_dict["table_ytno"].grid.get_field("course_code").get_query = function (doc) {
			var courses_list = [];
			$.each(doc.table_ytno, function (idx, val) {
				if (val.course_code) courses_list.push(val.course_code);
			});
			return { filters: [["Course Specification", "name", "not in", courses_list]] };
		};
	},
});

// get course required

frappe.ui.form.on("Program Specification", {
	refresh: function (frm) {
		// إضافة زر "Get Required Courses"
		frm.add_custom_button(__("Get Required Courses"), function () {
			frm.call({
				method: "get_required_courses",
				args: {
					doc: frm.doc,
				},
				freeze: true,
				freeze_message: __("Fetching courses..."),
				callback: function (r) {
					if (r.message) {
						// تحديث جدول table_ytno
						frm.clear_table("table_ytno");
						r.message.forEach(function (course) {
							let row = frm.add_child("table_ytno");
							row.course_code = course.course_code;
							row.course_name = course.course_name;
							row.course_type = course.course_type;
							row.study_level = course.study_level;
							row.semester = course.semester;
							row.elective = course.elective;
							row.source = course.source;
						});
						frm.refresh_field("table_ytno");
						frappe.msgprint(__("Courses fetched successfully!"));
					}
				},
			});
		}).addClass("btn-primary");
	},
});

// second try

// frappe.ui.form.on("Program Specification", {
//     refresh: function (frm) {
//         // إضافة زر "Get Required Courses"
//         frm.add_custom_button(__('Get Required Courses'), function () {
//             frm.call({
//                 method: "get_required_courses",
//                 args: {
//                     doc: frm.doc
//                 },
//                 freeze: true,
//                 freeze_message: __("Fetching courses..."),
//                 callback: function (r) {
//                     if (r.message) {
//                         // تحقق من المواد الموجودة في الجدول قبل إضافة المواد الجديدة
//                         let existing_courses = frm.doc.table_ytno.map(row => row.course_code);
//                         let new_courses = r.message.filter(course => !existing_courses.includes(course.course_code));

//                         if (new_courses.length > 0) {
//                             // إضافة المواد المتبقية للجدول
//                             new_courses.forEach(function (course) {
//                                 let row = frm.add_child("table_ytno");
//                                 row.course_code = course.course_code;
//                                 row.course_name = course.course_name;
//                                 row.course_type = course.course_type;
//                                 row.study_level = course.study_level;
//                                 row.semester = course.semester;
//                                 row.elective = course.elective;
//                                 row.source = course.source;
//                             });
//                             frm.refresh_field("table_ytno");
//                             frappe.msgprint(__("Courses added successfully!"));
//                         } else {
//                             frappe.msgprint(__("All required courses are already present in the study plan."));
//                         }
//                     }
//                 }
//             });
//         }).addClass('btn-primary');
//     },

//     // التحقق قبل الحفظ
//     before_save: function (frm) {
//         frm.call({
//             method: "validate_courses_in_plan",
//             args: {
//                 doc: frm.doc
//             },
//             freeze: true,
//             freeze_message: __("Validating courses..."),
//             callback: function (r) {
//                 if (r.message) {
//                     // إذا كانت المواد ناقصة سيتم عرض رسالة للمستخدم.
//                     frappe.msgprint(r.message);
//                     frappe.validated = false;  // منع الحفظ
//                 }
//             }
//         });
//     }
// });
