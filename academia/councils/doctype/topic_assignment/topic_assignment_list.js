frappe.listview_settings["Topic Assignment"] = {

  onload: function (topic_assignment) {

    topic_assignment.page.add_action_item(__('Add to Group'), function () {
      const selected_assignments = topic_assignment.get_checked_items(true);
      // Ensure there are selected assignments
      if (selected_assignments.length < 1) {
        frappe.msgprint(__('Please select at least one Topic Assignment to add to a group.'));
        return;
      }
      const dialog = new frappe.ui.Dialog({
        title: 'Choose Group',
        fields: [
          {
            label: 'Group assignment',
            fieldname: 'parent_assignment',
            fieldtype: 'Link',
            options: 'Topic Assignment',
            get_query: function () {
              return {
                filters: {
                  is_group: 1
                }
              };
            }
          }
        ],
        size: 'small',
        primary_action_label: 'Choose',
        primary_action(values) {
          frappe.call({
            method: "academia.councils.doctype.topic_assignment.topic_assignment.add_assignments_to_group",
            args: {
              parent_name: values.parent_assignment,
              assignments: JSON.stringify(selected_assignments)
            },
            callback: function (response) {
              if (response.message === "ok") {
                frappe.show_alert({
                  message: __('Assignment/s added successfully.'),
                  indicator: 'green'
                });
                cur_list.refresh();
              } else {
                frappe.show_alert({
                  message: __('Error adding assignments!'),
                  indicator: 'red'
                });
                console.error(response.message);
              }
            },
          });
          dialog.hide();
        }
      });
      dialog.show();
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
    return [
      __(doc.status),
      status_colors[doc.status],
      "status,=," + doc.status,
    ];
  },
};
