app_name = "academia"
app_title = "Academia"
app_publisher = "SanU"
app_description = "Academic institution management system"
app_email = "a.alshalabi@su.edu.ye"
app_license = "mit"
required_apps = ["frappe/erpnext", "frappe/hrms"]


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_js = "academia.bundle.js"
# app_include_css = "/assets/academia/css/academia.css"
# app_include_js = "/assets/academia/js/academia.js"

# include js, css files in header of web template
# web_include_css = "/assets/academia/css/academia.css"
# web_include_js = "/assets/academia/js/academia.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "academia/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "academia/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# "Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# "methods": "academia.utils.jinja_methods",
# "filters": "academia.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "academia.install.before_install"
# after_install = "academia.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "academia.uninstall.before_uninstall"
# after_uninstall = "academia.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "academia.utils.before_app_install"
# after_app_install = "academia.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "academia.utils.before_app_uninstall"
# after_app_uninstall = "academia.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "academia.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# "Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# "Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# "ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# "*": {
# "on_update": "method",
# "on_cancel": "method",
# "on_trash": "method"
# }
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# "all": [
# "academia.tasks.all"
# ],
# "daily": [
# "academia.tasks.daily"
# ],
# "hourly": [
# "academia.tasks.hourly"
# ],
# "weekly": [
# "academia.tasks.weekly"
# ],
# "monthly": [
# "academia.tasks.monthly"
# ],
# }

# Testing
# -------

before_tests = "academia.tests.test_utils.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# "frappe.desk.doctype.event.event.get_events": "academia.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# "Task": "academia.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["academia.utils.before_request"]
# after_request = ["academia.utils.after_request"]

# Job Events
# ----------
# before_job = ["academia.utils.before_job"]
# after_job = ["academia.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# {
# "doctype": "{doctype_1}",
# "filter_by": "{filter_by}",
# "redact_fields": ["{field_1}", "{field_2}"],
# "partial": 1,
# },
# {
# "doctype": "{doctype_2}",
# "filter_by": "{filter_by}",
# "partial": 1,
# },
# {
# "doctype": "{doctype_3}",
# "strict": False,
# },
# {
# "doctype": "{doctype_4}"
# }
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# "academia.auth.validate"
# ]
export_python_type_annotations = True


fixtures = [
	# Print formats
	{"doctype": "Print Format", "filters": [["name", "in", ["transaction"]]]},
	# Standard Fixtures
	"Academic Status",
	"Journal Type",
	"Workflow",
	"Workflow State",
	"Workflow Action Master",
	# Roles
	{"doctype": "Role", "filters": [["name", "in", ["Academic User", "Faculty Dean", "Department Head"]]]},
	# Custom DocPerm Fixtures
	{
		"doctype": "Custom DocPerm",
		"filters": [
			[
				"parent",
				"in",
				[
					"Course",
					"Student Group Tool",
					"Lesson",
					"Lesson Template",
					"Student Group",
					"Academic Year",
					"Academic Specialty",
					"Study Method",
					"Program Degree",
					"Student Category",
					"Appreciation Type",
					"Authority",
					"Scientific Degree",
					"Nationality",
					"Consultation Type",
					"Lecture",
					"Study Plan",
					"Semester",
					"Level",
					"Academic Term",
					"Student State",
					"Student",
					"Academic Rank",
					"Academic Publication",
					"Building",
					"Lab Type",
					"Room",
					"Scientific Article",
					"Lab",
					"Faculty Department",
					"Academic Program",
					"Student Batch",
					"Hour Type",
					"Level And Semester Enrollment",
					"Program Specification",
					"Tenure Evaluation Request",
					"Faculty Member",
					"Faculty",
					"Group Assignment Tool",
					"Group Assignment",
					"Academic Publication Type",
					"Academic Services",
					"Evaluation Criteria Template",
					"Tenure Request",
					"Evaluation Criterion",
					"Program Enrollment",
					"Course Specification",
					"Facility",
					"Schedule Template Version",
					"University",
					"Course Enrollment Tool",
					"Course Study",
					"Academic Status",
					"Faculty Need",
					"Degree Accreditation",
					"Journal",
					"Journal Type",
					"Course Study Tool",
					"Asset Access Request",
					"Student Admission",
					"Academic Attendance Tool",
					"Course Enrollment",
					"LMS Quiz",
					"Lesson Attendance",
					"Student Applicant",
					"Question",
					"Quiz Attempt",
					"Quiz Result",
					"LMS Assignment",
					"Academic Attendance Tool",
					"Semester Enrollment",
				],
			]
		],
	},
]
