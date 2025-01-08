frappe.listview_settings["Specific Transaction Document Action"] = {
	onload: function () {
		$(".btn-primary")
			.filter(function () {
				return $(this).text().trim() === "Add Specific Transaction Document Action";
			})
			.hide();
	},
};
