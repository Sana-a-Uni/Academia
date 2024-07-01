// Copyright (c) 2024, SanU Development Team and contributors
// For license information, please see license.txt

frappe.ui.form.on('External Entity', {
    onload: function(frm) {
      frm.set_query("parent_external_entity", function() {
        return {"filters": [
          ["External Entity", "is_group", "=", 1],
          // TODO: instead of this when check the is_group make the parent null
          ['External Entity', 'parent_external_entity', '=', ''],  // Only show parties without a parent
        ]};
        
      });
    },
});



