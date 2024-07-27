frappe.listview_settings["Lesson Attendance"] = {
    onload: function (list_view) {
	
		list_view.page.add_inner_button(__("Mark Attendance"), function () {
                frappe.set_route('Form','Academic Attendance Tool')
		});
	},
}