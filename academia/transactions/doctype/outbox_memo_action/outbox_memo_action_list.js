frappe.listview_settings["Outbox Memo Action"] = {
	onload: function () {
		$(".btn-primary")
			.filter(function () {
				return $(this).text().trim() === "Add Outbox Memo Action";
			})
			.hide();
	},
};
