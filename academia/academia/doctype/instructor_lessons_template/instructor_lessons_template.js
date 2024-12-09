// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt
frappe.ui.form.on("Instructor Lessons Template", {
	refresh: function (frm) {
		if (frm.doc.instructor && frm.doc.faculty && frm.doc.schedule_template_version) {
			// استدعاء دالة Python لجلب البيانات مع الفلتر الجديد
			frappe.call({
				method: "academia.academia.doctype.instructor_lessons_template.instructor_lessons_template.get_lessons_data",
				args: {
					instructor: frm.doc.instructor,
					faculty: frm.doc.faculty,
					schedule_template_version: frm.doc.schedule_template_version, // إضافة الفلتر الجديد
				},
				callback: function (r) {
					if (r.message) {
						const lessons = r.message;

						// إنشاء الجدول ديناميكياً
						let tableHTML = `
                          <div dir="rtl">
                            <table border="1" style="width: 100%; text-align: center; border-collapse: collapse;">
                              <tr>
                                <th> </th>
                                <th> 1  <br> 08:00 - 10:00</th>
                                <th> 2  <br> 10:00 - 12:00</th>
                                <th> 3  <br> 12:00 - 14:00</th>
                                <th> 4  <br> 14:00 - 16:00</th>
                                <th> 5  <br> 16:00 - 18:00</th>
                              </tr>
                      `;

						// التكرار على الأيام والفترات الزمنية
						Object.keys(lessons).forEach((day) => {
							tableHTML += `<tr><th>${day}</th>`; // إضافة اليوم
							lessons[day].forEach((slot) => {
								if (slot) {
									// تنسيق البيانات داخل الخلية
									tableHTML += `
                                      <td>
                                          <div style="text-align: right; font-size: smaller; margin-bottom: 5px;">
                                              ${slot.group || ""}
                                          </div>
                                          <div style="text-align: center; font-size: medium; font-weight: bold;">
                                              ${slot.course || ""}
                                          </div>
                                          <div style="text-align: right; font-size: smaller; margin-top: 5px;">
                                              ${slot.instructor || ""}
                                          </div>
                                          <div style="text-align: left; font-size: smaller; margin-top: 5px;">
                                              ${slot.room || ""}
                                          </div>
                                      </td>
                                  `;
								} else {
									tableHTML += `<td></td>`; // خلية فارغة
								}
							});
							tableHTML += `</tr>`;
						});

						tableHTML += `
                            </table>
                          </div>
                      `;

						// تحديث الحقل HTML بالجدول
						frm.fields_dict.lessons.$wrapper.html(tableHTML);
					} else {
						// في حالة عدم وجود بيانات
						frm.fields_dict.lessons.$wrapper.html(
							'<div style="text-align: center;">No lessons found for the selected instructor and faculty.</div>'
						);
					}
				},
				error: function () {
					// في حالة حدوث خطأ
					frm.fields_dict.lessons.$wrapper.html(
						'<div style="text-align: center; color: red;">An error occurred while fetching the lessons.</div>'
					);
				},
			});
		} else {
			// رسالة توجيهية للمستخدم إذا لم يتم اختيار Instructor أو Faculty أو Schedule Template Version
			frm.fields_dict.lessons.$wrapper.html(
				'<div style="text-align: center;">Please select an Instructor, Faculty, and Schedule Template Version.</div>'
			);
		}
	},

	instructor: function (frm) {
		frm.trigger("refresh"); // تحديث الجدول عند تغيير المدرس
	},

	faculty: function (frm) {
		frm.trigger("refresh"); // تحديث الجدول عند تغيير الكلية
	},

	schedule_template_version: function (frm) {
		frm.trigger("refresh"); // تحديث الجدول عند تغيير النسخة
	},
});
