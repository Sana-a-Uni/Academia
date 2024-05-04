frappe.listview_settings["Topic Assignment"] = {
  has_indicator_for_draft: 1,
  get_indicator: function (doc) {
    const status_colors = {
      "Pending Review": "orange",
      "Pending Acceptance": "blue",
      Accepted: "green",
      Rejected: "red",
    };
    return [
      __(doc.status),
      status_colors[doc.status],
      "status,=," + doc.status,
    ];
  },
};
