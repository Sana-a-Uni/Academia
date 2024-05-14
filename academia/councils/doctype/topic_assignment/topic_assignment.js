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

  onload: function(frm) {
      // Hide the grouped_assignments field initially
      frm.toggle_display('grouped_assignments', false);
  },
  is_group: function(frm) {
      // Check the value of the checkbox field
      if (frm.doc.is_group) {
          // If checkbox is checked, display the grouped_assignments field
          frm.toggle_display('grouped_assignments', true);
      } else {
          // If checkbox is unchecked, hide the grouped_assignments field
          frm.toggle_display('grouped_assignments', false);
      }
  },

    refresh: function(frm) {
      frm.set_query("parent_assignment", function(doc) {
        return {
          filters: [
            ["is_group", "=",1]
          ]
        };
      });
      
      frm.set_query("topic_assignment_","grouped_assignments", function(doc) {
        return {
          filters: [
            ["is_group", "=", 0]
          ]
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
      title:null,
      main_category:null,
      sub_category:null,
      assignment_date:null,
      },
      add_filters_group: 1,
      date_field: "transaction_date",
      // columns: ["title","main_category"],
      get_query() {
          return{ 
            filters: { is_group: ['=', 0] }
          }
      },
      action(selections) {
          console.log(selections);
      },
    
      primary_action_label: "Get Assignments To Group",
      action(selections) {
        frm.set_value('grouped_assignments', []);
        selections.forEach((assignment, index, array) => {
          frappe.db.get_value("Topic Assignment", assignment, "title", (obj) => {
            if (obj) {
              frm.add_child("grouped_assignments", {
                obj: assignment,
                title: obj.title,
              })
              console.log(`array => ${array}`)
              if (index === array.length - 1) {
                frm.refresh_field("grouped_assignments");
              }
            }
          });
        });
        this.dialog.hide();
      },
    });
    }
});

