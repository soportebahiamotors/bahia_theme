app_name = "bahia_theme"
app_title = "Bahia Theme"
app_publisher = "Bahia Motors"
app_description = "Tema visual corporativo (colores de marca) para el Desk de ERPNext en Bahia Motors"
app_email = "jean.guerrel@bahiamotors.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "bahia_theme",
# 		"logo": "/assets/bahia_theme/logo.png",
# 		"title": "Bahia Theme",
# 		"route": "/bahia_theme",
# 		"has_permission": "bahia_theme.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/bahia_theme/css/bahia_theme.css"
# app_include_js = "/assets/bahia_theme/js/bahia_theme.js"

# include js, css files in header of web template
# web_include_css = "/assets/bahia_theme/css/bahia_theme.css"
# web_include_js = "/assets/bahia_theme/js/bahia_theme.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "bahia_theme/public/scss/website"

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
# app_include_icons = "bahia_theme/public/icons.svg"

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

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Fixtures
# --------
# Config custom (Roles/permisos/Workspaces/Users) que vive solo en la base de
# MariaDB del servidor y que un rebuild de imagen Docker perdería si no queda
# declarada acá (ver incidente del 16-sep-2026: un rebuild + bench migrate
# borro 4 Workspace/Desktop Icon custom que no estaban trackeados como fixture
# de ninguna app). Regenerar con:
#   bench --site frontend export-fixtures
fixtures = [
	# Modulos custom migrados de GeneXus (shell Workspace + sidebar + tile)
	{"dt": "Workspace", "filters": [["name", "in", ["Autos", "Citas Taller", "Taller"]]]},
	{"dt": "Workspace Sidebar", "filters": [["name", "in", ["Autos", "Citas Taller", "Taller"]]]},
	{"dt": "Desktop Icon", "filters": [["name", "in", ["Autos", "Citas Taller", "Taller"]]]},
	# Role de solo lectura para integraciones (bot.comparador@bahiamotors.com)
	{"dt": "Role", "filters": [["name", "in", ["Comparador Solo Lectura"]]]},
	{"dt": "Custom DocPerm", "filters": [["role", "=", "Comparador Solo Lectura"]]},
	{"dt": "User", "filters": [["name", "in", ["bot.comparador@bahiamotors.com"]]]},
]
