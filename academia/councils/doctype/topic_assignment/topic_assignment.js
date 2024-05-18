// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Topic Assignment", {
  setup: function (frm) {
    $(`<style>
      .btn[data-fieldname="get_data_from_topic"] {
        background-color: #171717; /* Custom dark gray */
        color: white;
      }
      .btn[data-fieldname="get_data_from_topic"]:hover {
        background-color: #171710 !important;/* Slightly darker gray for interaction states */
        color: white !important;
      }
    </style>`).appendTo("head");

    frm.add_fetch("topic", "topic_main_category", "main_category");
    frm.add_fetch("topic", "topic_sub_category", "sub_category");
  },

  onload: function (frm) {
    frm.events.topic_filters(frm);
    // frm.set_df_property("topic", "placeholder", "Council must be filled");
    frm.refresh_field("grouped_assignments");
    // Hide the grouped_assignments field initially
    frm.toggle_display("grouped_assignments", false);
  },

  topic_filters: function (frm) {
    frm.set_query("topic", function () {
      return {
        query:
          "academia.councils.doctype.topic_assignment.topic_assignment.get_available_topics",
        filters: {
          council: frm.doc.council,
          docstatus: 1,
          status: ["Complete", "In Progress"],
        },
      };
    });
  },

  is_group: function (frm) {
    // Check the value of the checkbox field
    if (frm.doc.is_group) {
      frm.events.clear_topic(frm); // clear topic field which will also clear the main and sub category fields if user enable is_group checkbox
      // If checkbox is checked, display the grouped_assignments field
      frm.toggle_display("grouped_assignments", true);
    } else {
      frm.set_value("main_category", ""); //clear catetories if user disable is_group checkbox
      frm.set_value("sub_category", "");
      // If checkbox is unchecked, hide the grouped_assignments field
      frm.toggle_display("grouped_assignments", false);
    }
  },

  refresh: function (frm) {
    frm.set_query("parent_assignment", function () {
      return {
        filters: {
          council: frm.doc.council,
          is_group: 1,
          decision_type: "", //empty ,not set , means assignment not scheduled for session
        },
      };
    });

    frm.set_query("topic_assignment", "grouped_assignments", function (doc) {
      return {
        filters: {
          council: frm.doc.council,
          is_group: 1,
          decision_type: "", //empty ,not set , means assignment not scheduled for session
        },
      };
    });
  },

  council: function (frm) {
    frm.events.clear_topic(frm);
  },

  main_category(frm) {
    // Update the options for the sub-category field based on the selected main category
    frm.set_query("sub_category", function () {
      return {
        filters: {
          topic_main_category: frm.doc.main_category,
        },
      };
    });
  },

  get_data_from_topic: function (frm) {
    if (frm.doc.topic) {
      // Manually fetch the title and description from the "Topic" DocType
      frappe.db
        .get_value("Topic", { name: frm.doc.topic }, ["title", "description"])
        .then((r) => {
          if (r.message) {
            // Manually set the fetched values to the form fields
            frm.set_value("title", r.message.title);
            frm.set_value("description", r.message.description);
          }
        });
    }
  },

  clear_topic: function (frm) {
    frm.set_value("topic", "");
    frm.refresh_field("topic");
  },

  get_assignments_to_group: function (frm) {
    new frappe.ui.form.MultiSelectDialog({
      doctype: "Topic Assignment",
      target: frm,
      setters: {
        title: null,
        main_category: null,
        sub_category: null,
        assignment_date: null,
      },
      add_filters_group: 1,
      // date_field: "transaction_date",
      // columns: ["title","main_category"],
      get_query() {
        return {
          filters: {
            is_group: 0,
            council: frm.doc.council,
            decision_type: "", //empty ,not set , means assignment not scheduled for session
            // status:"Accepted"
          },
        };
      },
      action(selections) {
        console.log(selections);
      },

      primary_action_label: "Get Assignments To Group",
      action(selections) {
        frm.set_value("grouped_assignments", []);
        selections.forEach((assignment, index, array) => {
          frappe.db.get_value(
            "Topic Assignment",
            assignment,
            ["name", "title", "assignment_date"],
            (obj) => {
              if (obj) {
                frm.add_child("grouped_assignments", {
                  obj: assignment,
                  topic_assignment: obj.name,
                  title: obj.title,
                  assignment_date: obj.assignment_date,
                });
                if (index === array.length - 1) {
                  frm.refresh_field("grouped_assignments");
                }
              }
            }
          );
        });
        this.dialog.hide();
      },
    });
  },
  // after_save: function(frm) {
  //   frm.doc.grouped_assignments.forEach(function(assignment) {
  //   frappe.db.set_value("Topic Assignment", assignment.topic_assignment, 'parent_assignment', frm.doc.name);
  // });
  // }
});
