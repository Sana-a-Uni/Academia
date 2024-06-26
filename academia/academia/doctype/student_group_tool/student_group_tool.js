// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

   frappe.ui.form.on("Student Group Tool", {
 	onload: function(frm) {
 	
 	    const urlParams = new URLSearchParams(window.location.search);
 	    //const based_on = urlParams.get('based_on');
 	    //const capacity = urlParams.get('capacity');
		const student_group = urlParams.get('student_group');
		const based_on = urlParams.get('based_on');
 	    
 	     if (based_on) {
 	     	frm.set_value('based_on', based_on);
 	     }
 	    // if (capacity) {
 	    // 	frm.set_value('capacity', capacity);
 	    // }
		 if (student_group) {
			frm.set_value('student_group', student_group);
		}

 	}
   });
