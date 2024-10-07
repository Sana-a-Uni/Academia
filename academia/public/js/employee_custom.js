//1- the filter of academic department
frappe.ui.form.on('Employee', {
	refresh: function (frm) {
		frm.set_query('custom_academic_department', function () {
			return {
				filters: {
					'custom_faculty': frm.doc.custom_faculty,
					'custom_is_academic_department': 1
				}	
			};
		});
	}
});
// END filter of academic department


//2- custom get years of work for employee by date_of_joining
frappe.ui.form.on('Employee', {
	// refresh: function (frm) {

	// },
	onload: function (frm) {
		if (frm.doc.date_of_joining) {
			$(frm.fields_dict['custom_years_of_service'].wrapper).html("Your years of service : " + get_years_work(frm.doc.date_of_joining));
		}
	}
});

frappe.ui.form.on("Employee", "date_of_joining", function (frm) {
	if (frm.doc.date_of_joining) {
		var today = new Date();
		var joinDate = new Date(frm.doc.date_of_birth);
		var age_str = get_years_work(frm.doc.date_of_joining);
		$(frm.fields_dict['custom_years_of_service'].wrapper).html("Your years of service : " + age_str);
	}
});

var get_years_work = function (joining) {
	var ageMS = Date.parse(Date()) - Date.parse(joining);
	var age = new Date();
	age.setTime(ageMS);
	var years = age.getFullYear() - 1970;
	return years + "Year (s)";
};

// end custom years of work

// 3 - custom get age for employee by date_of_birth
frappe.ui.form.on('Employee', {
	// refresh: function (frm) {

	// },
	onload: function (frm) {
		if (frm.doc.date_of_birth) {
			$(frm.fields_dict['custom_age'].wrapper).html("AGE : " + get_age(frm.doc.date_of_birth));
		}
	}
});

frappe.ui.form.on("Employee", "date_of_birth", function (frm) {
	if (frm.doc.date_of_birth) {
		var today = new Date();
		var birthDate = new Date(frm.doc.date_of_birth);
		var age_str = get_age(frm.doc.date_of_birth);
		$(frm.fields_dict['custom_age'].wrapper).html("Your AGE : " + age_str);
	}
});

var get_age = function (birth) {
	var ageMS = Date.parse(Date()) - Date.parse(birth);
	var age = new Date();
	age.setTime(ageMS);
	var years = age.getFullYear() - 1970;
	return years + " Year(s) " + age.getMonth() + " Month(s) " + age.getDate() + " Day(s)";
};
// end custom age

