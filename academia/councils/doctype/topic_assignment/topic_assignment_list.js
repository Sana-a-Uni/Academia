frappe.listview_settings["Topic Assignment"] = {

  onload: function (topic_assignment) {

    topic_assignment.page.add_action_item(__('Add to Group'), async function () {
      const selected_assignments = topic_assignment.get_checked_items(true);
      if (selected_assignments.length < 2) {
        frappe.msgprint(__('Please select two or more Topic Assignments to add a group.'));
        return;
      }

      await frappe.model.with_doctype('Topic Assignment');
      var doc = frappe.model.get_new_doc('Topic Assignment');
      doc.is_group = 1;
      let errors = [];

      for (let assignment of selected_assignments) {
        try {
          let { message: obj } = await frappe.db.get_value(
            "Topic Assignment",
            assignment,
            ["title",
              "assignment_date",
              "is_group",
              "parent_assignment"
            ]
          );
          if (obj) {
            if (obj.is_group) {
              errors.push(`Assignment ${assignment} is a group and can't be added to another group.`);
            } else if (obj.parent_assignment) {
              errors.push(`Assignment ${assignment} is already part of another group.`);
            } else {
              let new_child = frappe.model.add_child(
                doc,
                'Topic Assignment Copy',
                'grouped_assignments'
              );
              new_child.topic_assignment = assignment;
              new_child.title = obj.title;
              new_child.assignment_date = obj.assignment_date;
            }
          }
        } catch (error) {
          console.error(`Error fetching assignment ${assignment}:`, error);
          errors.push(`Error fetching assignment ${assignment}`);
        }
      }
      if (errors.length > 0) {
        frappe.msgprint({
          title: __('Validation Errors'),
          message: errors.join('<br>'),
          indicator: 'red'
        });
        return;
      }

      frappe.set_route('Form', 'Topic Assignment', doc.name);
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
