frappe.listview_settings["Topic"] = {
  has_indicator_for_draft: 1,
  get_indicator: function (doc) {
    const status_colors = {
      Open: "blue",
      Complete: "green",
      "In Progress": "orange",
      Hold: "gray",
      Closed: "red",
    };

    return [
      __(doc.status),
      status_colors[doc.status],
      "status,=," + doc.status,
    ];
  },
};
