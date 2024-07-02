// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

   frappe.ui.form.on("Student Group", {
   	refresh: function(frm) {
   		if (frm.fields_dict.go_to) {
	    	    frm.fields_dict.go_to.$input.on('click', function() {
					const student_group_name = frm.doc.student_group_name;
					const group_based_on = frm.doc.group_based_on;
					const grouping_by = 'Practical';
					//frappe.msgprint(student_group_name);
	    	    	const url = frappe.urllib.get_full_url(__("/app/student-group-tool?student_group={0}&based_on={1}&grouping_by={2}",[student_group_name,group_based_on,grouping_by]));
					frappe.msgprint(url);
	    		//frappe.set_route('Form', 'Student Group Tool');
	    		window.open(url, '_blank');
	    	    });
	    	}
   	}
   });
