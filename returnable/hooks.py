# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "returnable"
app_title = "Returnable"
app_publisher = "Warehouseman"
app_description = "ERPNext module for serial numbered returnable containers"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "mhb.warehouseman@gmail.com"
app_license = "MIT"

fixtures = [
  { "dt": "Custom Field", "filters": [["fieldname", "in", ("returnables", "holdings")]]}
]


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/returnable/css/returnable.css"
# app_include_js = "/assets/returnable/js/returnable.js"

# include js, css files in header of web template
# web_include_css = "/assets/returnable/css/returnable.css"
# web_include_js = "/assets/returnable/js/returnable.js"

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

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Delivery Note": {
        "validate": "returnable.hook_tasks.startStockEntry"
    }
}

# doc_events = {
#   "*": {
#       "on_update": "method",
#       "on_cancel": "method",
#       "on_trash": "method"
#   }
# }

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "returnable.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "returnable.install.before_install"
# after_install = "returnable.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "returnable.notifications.get_notification_config"

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

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"returnable.tasks.all"
# 	],
# 	"daily": [
# 		"returnable.tasks.daily"
# 	],
# 	"hourly": [
# 		"returnable.tasks.hourly"
# 	],
# 	"weekly": [
# 		"returnable.tasks.weekly"
# 	]
# 	"monthly": [
# 		"returnable.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "returnable.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "returnable.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "returnable.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

