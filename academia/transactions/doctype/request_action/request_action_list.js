frappe.listview_settings["Request Action"] = {
	onload: function () {
		$(".btn-primary")
			.filter(function () {
				return $(this).text().trim() === "Add Request Action";
			})
			.hide();
	},
};
