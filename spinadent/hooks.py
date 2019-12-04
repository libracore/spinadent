# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "spinadent"
app_title = "Spinadent"
app_publisher = "libracore"
app_description = "ERPNext applications for Spinadent"
app_icon = "octicon octicon-beaker"
app_color = "#172bed"
app_email = "info@libracore.com"
app_license = "AGPL"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/spinadent/css/spinadent.css"
# app_include_js = "/assets/spinadent/js/spinadent.js"

# include js, css files in header of web template
# web_include_css = "/assets/spinadent/css/spinadent.css"
# web_include_js = "/assets/spinadent/js/spinadent.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "spinadent.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "spinadent.install.before_install"
# after_install = "spinadent.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "spinadent.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"spinadent.tasks.all"
# 	],
# 	"daily": [
# 		"spinadent.tasks.daily"
# 	],
# 	"hourly": [
# 		"spinadent.tasks.hourly"
# 	],
# 	"weekly": [
# 		"spinadent.tasks.weekly"
# 	]
# 	"monthly": [
# 		"spinadent.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "spinadent.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "spinadent.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "spinadent.task.get_dashboard_data"
# }

