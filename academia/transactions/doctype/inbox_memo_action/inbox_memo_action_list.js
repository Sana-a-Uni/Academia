frappe.listview_settings["Inbox Memo Action"] = {
	onload: function () {
		$(".btn-primary")
			.filter(function () {
				return $(this).text().trim() === "Add Inbox Memo Action";
			})
			.hide();
	},
};
