frappe.listview_settings["Topic"] = {
	onload: function (topic) {
		topic.page.add_action_item(__("Add to Group"), function () {
			const selected_topics = topic.get_checked_items(true);
			// Ensure there are selected topics
			if (selected_topics.length < 1) {
				frappe.msgprint(__("Please select at least one Topic to add to a group."));
				return;
			}
			const dialog = new frappe.ui.Dialog({
				title: __("Choose Group"),
				fields: [
					{
						label: "Group Topic",
						fieldname: "parent_topic",
						fieldtype: "Link",
						options: "Topic",
						get_query: function () {
							return {
								filters: {
									is_group: 1,
								},
							};
						},
					},
				],
				size: "small",
				primary_action_label: __("Choose"),
				primary_action(values) {
					frappe.call({
						method: "academia.councils.doctype.topic.topic.add_topics_to_group",
						args: {
							parent_name: values.parent_topic,
							topics: JSON.stringify(selected_topics),
						},
						callback: function (response) {
							if (response.message === "ok") {
								frappe.show_alert({
									message: __("Topic(s) added successfully."),
									indicator: "green",
								});
								cur_list.refresh();
							} else {
								frappe.show_alert({
									message: __("Error adding topics!"),
									indicator: "red",
								});
								console.error(response.message);
							}
						},
					});
					dialog.hide();
				},
			});
			dialog.show();
		});

		topic.page.add_action_item(__("Add to New Group"), function () {
			const selected_topics = topic.get_checked_items();

			frappe.call({
				method: "academia.councils.doctype.topic.topic.create_new_group",
				freeze: true,
				args: {
					topics: selected_topics,
				},
				callback: function (r) {
					if (r.message) {
						frappe.show_alert({
							message: __("Group created and Topic(s) added successfully."),
							indicator: "green",
						});
						var doc = frappe.model.sync(r.message)[0];
						frappe.set_route("Form", doc.doctype, doc.name);
					} else {
						frappe.show_alert({
							message: __("Error creating group or adding topics!"),
							indicator: "red",
						});
					}
				},
			});
		});
	},

	has_indicator_for_draft: 1,
	get_indicator: function (doc) {
		const status_colors = {
			"Pending Review": "orange",
			"Pending Acceptance": "blue",
			Accepted: "green",
			Rejected: "red",
		};
		return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
	},
};
