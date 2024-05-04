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
  },

  onload: function (frm) {
    frm.events.topic_filters(frm);
    // frm.set_df_property("topic", "placeholder", "Council must be filled");
  },

  topic_filters: function (frm) {
    frm.set_query("topic", function () {
      return {
        query:
          "academia.councils.doctype.topic_assignment.topic_assignment.get_available_topics",
        filters: { council: frm.doc.council },
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
});
