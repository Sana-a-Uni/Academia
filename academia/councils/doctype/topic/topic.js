// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Topic", {
	setup: function (frm) {
		$(`<style>
      .btn[data-fieldname="get_data_from_topic"] {
        background-color: #171717; /* Custom dark gray */
        color: white;
      }
      .btn[data-fieldname="get_data_from_topic"]:hover {
        background-color: #171710 !important; /* Slightly darker gray for interaction states */
        color: white !important;
      }
    </style>`).appendTo("head");

		frm.add_fetch("transaction", "category", "category");
	},

	onload: function (frm) {
		// frm.events.topic_filters(frm);
		// frm.set_df_property("topic", "placeholder", "Council must be filled");
	},

	// topic_filters: function (frm) {
	// 	frm.set_query("topic", function () {
	// 		return {
	// 			query: "academia.councils.doctype.topic.topic.get_available_topics",
	// 			filters: {
	// 				council: frm.doc.council,
	// 				docstatus: 1,
	// 				status: ["Complete", "In Progress"],
	// 			},
	// 		};
	// 	});
	// },
	is_group: function (frm) {
		if (frm.doc.is_group) {
			// frm.events.clear_topic(frm); // clear topic field which will also clear the main and sub category fields if user enable is_group checkbox
		} else {
			// frm.set_value("main_category", ""); //clear categories if user disable is_group checkbox
			// frm.set_value("sub_category", "");
		}
	},
	refresh: function (frm) {
		if (frm.is_new() || frm.doc.docstatus !== 0) {
			frm.toggle_display("get_topics_to_group", false);
		} else {
			frm.toggle_display("get_topics_to_group", true);
		}

		show_grouped_topics(frm);

		frm.set_query("sub_category", function () {
			return {
				filters: {
					parent_category: frm.doc.category,
				},
			};
		});

		frm.set_query("parent_topic", function () {
			return {
				filters: {
					council: frm.doc.council,
					is_group: 1,
					decision_type: "", //empty, not set, means topic not scheduled for session
					docstatus: 0, // draft
				},
			};
		});
	},

	council: function (frm) {
		// frm.events.clear_topic(frm);
	},

	// main_category(frm) {
	// 	// Update the options for the sub-category field based on the selected main category
	// 	frm.set_query("sub_category", function () {
	// 		return {
	// 			filters: {
	// 				main_category: frm.doc.main_category,
	// 			},
	// 		};
	// 	});
	// },

	// get_data_from_topic: function (frm) {
	// 	if (frm.doc.topic) {
	// 		// Manually fetch the title and description from the "Topic" DocType
	// 		frappe.db
	// 			.get_value("Topic", { name: frm.doc.topic }, ["title", "description"])
	// 			.then((r) => {
	// 				if (r.message) {
	// 					// Manually set the fetched values to the form fields
	// 					frm.set_value("title", r.message.title);
	// 					frm.set_value("description", r.message.description);
	// 				}
	// 			});
	// 	}
	// },

	// clear_topic: function (frm) {
	// 	frm.set_value("topic", "");
	// 	frm.refresh_field("topic");
	// },

	get_topics_to_group: function (frm) {
		new frappe.ui.form.MultiSelectDialog({
			doctype: "Topic",
			target: frm,
			setters: {
				title: null,
				category: null,
				topic_date: null,
			},
			add_filters_group: 1,
			// date_field: "transaction_date",
			// columns: ["title","main_category"],
			get_query() {
				return {
					filters: {
						is_group: 0,
						council: frm.doc.council,
						parent_topic: "",
						decision_type: "", //empty, not set, means topic not scheduled for session
						docstatus: 0, // draft
						// status:"Pending"
					},
				};
			},
			primary_action_label: __("Get Topics To Group"),
			action: function (selections) {
				frappe.call({
					method: "academia.councils.doctype.topic.topic.add_topics_to_group",
					args: {
						parent_name: frm.doc.name,
						topics: JSON.stringify(selections), // Convert the selections array to a JSON string
					},
					callback: function (response) {
						if (response.message === "ok") {
							show_grouped_topics(frm);
							frappe.show_alert({
								message: __("Topic(s) added successfully."),
								indicator: "green",
							});
						} else {
							frappe.show_alert({
								message: __(`Error adding topics!`),
								indicator: "red",
							});
							console.error(response.message);
						}
					},
					error: function (error) {
						console.error(error);
						frappe.show_alert({
							message: __("Error adding topics!"),
							indicator: "red",
						});
					},
				});
				this.dialog.hide();
			},
		});
	},
});

function show_grouped_topics(frm) {
	const container = $(frm.fields_dict.grouped_topics.wrapper);
	container.empty(); // Clear previous data

	if (frm.is_new()) {
		$(container).html(
			`<h3>${__("You should save this document before adding grouped topics!")}</h3>`
		);
		return;
	}

	fetch_topics_data(frm, function (data) {
		if (data.length > 0) {
			create_datatable(frm, container, data);
		} else {
			$(container).html(`<h3> ${__("No grouped topics added yet!")}</h3>`);
		}
	});
}

function fetch_topics_data(frm, callback) {
	frm.call({
		method: "get_grouped_topics",
		args: { parent_name: frm.doc.name },
		callback: function (r) {
			const data = r.message ? format_topic_data(r.message) : [];
			callback(data);
		},
	});
}

function format_topic_data(topics) {
	return topics.map((d) => [
		`<input type="checkbox" data-topic="${d.name}">`,
		`<a href='/app/topic/${d.name}'>${d.name}</a>`,
		d.title,
		frappe.datetime.str_to_user(d.topic_date),
		d.decision_type,
	]);
}

function create_datatable(frm, container, data) {
	const datatable = new DataTable(container[0], {
		columns: get_datatable_columns(),
		data: data,
		dynamicRowHeight: true,
		checkboxColumn: false,
		// inlineFilters: true,
	});

	datatable.style.setStyle(".dt-cell__content", { textAlign: "left" });

	const deleteButton = $("<button>")
		.text(__("Delete"))
		.addClass("btn btn-danger")
		.css({ marginBottom: "10px", visibility: "hidden" })
		.on("click", function () {
			const selectedRows = get_selected_rows();
			if (selectedRows.length > 0) {
				frappe.confirm(
					__("Are you sure you want to delete the selected topics?"),
					function () {
						handleDeletion(frm, selectedRows);
					}
				);
			}
		});

	container.append(deleteButton);

	container.on("change", "input[data-topic]", function () {
		const selectedRows = get_selected_rows();
		if (selectedRows.length > 0) {
			deleteButton.css("visibility", "visible"); // Correct property setting
		} else {
			deleteButton.css("visibility", "hidden"); // Correct property setting
		}
	});

	// Add event listener for the "Select All" checkbox
	container.on("change", 'input[data-topic1="All"]', function () {
		const isChecked = $(this).prop("checked");
		$("input[data-topic]")
			.not('[data-topic1="All"]')
			.prop("checked", isChecked)
			.trigger("change");
	});
}

function get_selected_rows() {
	const selectedRows = [];
	$("input[data-topic]:checked").each(function () {
		selectedRows.push($(this).data("topic"));
	});
	return selectedRows;
}

function get_datatable_columns() {
	return [
		{
			name: `<input type="checkbox" data-topic1="All">`,
			width: 50,
			editable: false,
			sortable: false,
		},
		{ name: __("Topic"), width: 300, editable: false },
		{ name: __("Title"), width: 300, editable: false },
		{ name: __("Topic Date"), width: 150, editable: false },
		{ name: __("Decision Type"), width: 143, editable: false },
	];
}
function delete_topics_from_group(frm, topic_names, callback) {
	frappe.call({
		method: "academia.councils.doctype.topic.topic.delete_topics_from_group",
		args: {
			topic_names: JSON.stringify(topic_names), // Convert the array to a JSON string
		},
		callback: function (response) {
			if (response.message === "ok") {
				callback(null);
			} else {
				callback(new Error(response.message));
			}
		},
		error: function (error) {
			callback(error);
		},
	});
}

function handleDeletion(frm, selectedRows) {
	delete_topics_from_group(frm, selectedRows, function (error) {
		if (error) {
			frappe.show_alert({
				message: __("Error removing topics!"),
				indicator: "red",
			});
			console.error(error);
		} else {
			frappe.show_alert({
				message: __("Topics removed successfully."),
				indicator: "green",
			});
			show_grouped_topics(frm);
		}
	});
}
