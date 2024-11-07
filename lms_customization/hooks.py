app_name = "lms_customization"
app_title = "Lms Customization"
app_publisher = "8848digital"
app_description = "LMS Customization"
app_email = "dev@8848digital.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/lms_customization/css/lms_customization.css"
# app_include_js = "/assets/lms_customization/js/lms_customization.js"

# include js, css files in header of web template
# web_include_css = "/assets/lms_customization/css/lms_customization.css"
# web_include_js = "/assets/lms_customization/js/lms_customization.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "lms_customization/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}
after_migrate = "lms_customization.migrate.after_migrate"

# include js in doctype views
doctype_js = {"LMS Course" : "lms_customization/customization/course/lms_course.js",
              }
update_website_context = [
	"lms_customization.widgets.update_website_context",
]
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "lms_customization/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "lms_customization.utils.jinja_methods",
# 	"filters": "lms_customization.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "lms_customization.install.before_install"
# after_install = "lms_customization.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "lms_customization.uninstall.before_uninstall"
# after_uninstall = "lms_customization.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "lms_customization.utils.before_app_install"
# after_app_install = "lms_customization.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "lms_customization.utils.before_app_uninstall"
# after_app_uninstall = "lms_customization.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "lms_customization.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"File": {
#         "after_insert": "lms_customization.lms_customization.customization.file_list.file_list.insert_file",
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"lms_customization.tasks.all"
# 	],
# "daily": [
# 	"lms_customization.lms_customization.customization.department.doc_events.utility.call_event_streaming",
#     "lms_customization.lms_customization.customization.department.doc_events.utility.sync_between_servers"
# ],
# 	"hourly": [
# 		"lms_customization.tasks.hourly"
# 	],
# 	"weekly": [
# 		"lms_customization.tasks.weekly"
# 	],
# 	"monthly": [
# 		"lms_customization.tasks.monthly"
# 	],
}

# Testing
# -------

# before_tests = "lms_customization.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"lms.lms.doctype.lms_course.lms_course.search_course": "lms_customization.lms_customization.customization.lms_course.search_filter.search_course",
    "lms.lms.doctype.lms_course.lms_course.save_course": "lms_customization.lms_customization.customization.lms_course.search_filter.save_course"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "lms_customization.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["lms_customization.utils.before_request"]
# after_request = ["lms_customization.utils.after_request"]

# Job Events
# ----------
# before_job = ["lms_customization.utils.before_job"]
# after_job = ["lms_customization.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"lms_customization.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
fixtures = [
        {"dt": "Doctype", "filters": [
                [
                    "name", "in", [
                        "Ride Add On",
                        "Ride Booking",
                        "Vehicle Ride"
                    ]
               ]
    ]}
]
