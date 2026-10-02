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
# Desactivado 2026-10-01: se instaló `swift_theme` (github.com/its-alikhokher/
# swift_theme) como orquestador principal de la parte visual del Desk
# (navbar, sidebar, listas, reportes, kanban, formularios, modales, login).
# Tanto bahia_theme.css como bahia_vanilla_theme.css pisaban navbar/sidebar/
# list view/botones/tipografía con !important — competían directo con
# swift_theme, así que se sacan de acá. Los archivos quedan en el repo
# (public/css/) por si el usuario quiere rescatar algo puntual de marca
# (colores de los 4 Desktop Icon sin SVG propio, zebra striping) una vez
# que swift_theme esté configurado, pero no se inyectan más.
# app_include_js = "/assets/bahia_theme/js/bahia_theme.js"

# Iconos de Autos/Citas Taller/Taller reaccionando al --swift-primary activo
# (ver bahia_theme_reactive_icons.css para el detalle) - acotado solo a esos
# 3 tiles via [data-id="..."] exacto, no reactiva bahia_theme.css ni
# bahia_vanilla_theme.css (siguen deshabilitados, ver nota de arriba: esos dos
# competian con swift_theme a lo ancho de todo el Desk).
#
# IMPORTANTE (2-oct-2026): el path ya empieza con "/assets", asi que
# frappe.utils.jinja_globals.bundled_asset() NUNCA lo hace pasar por
# assets.json (ese hash automatico solo aplica a paths que contienen
# ".bundle." Y que NO empiecen ya con "/assets" - ver el codigo fuente de esa
# funcion). Esto significa que esta URL es literalmente la misma de por vida,
# edites o no el CSS: swift_theme pasó por este mismo bug con su propio CSS
# ("every one was served from a URL that never changed, so browsers and nginx
# held the old copy across upgrades", comentario real en su
# swift_theme.bundle.scss) y lo resolvio moviendo su CSS a un nombre
# ".bundle." real con hash. Ac'a, en vez de migrar todo el pipeline, se usa un
# cache-busting manual mas simple: el "?v=N" al final. BUMPEAR ESE NUMERO EN
# CADA EDICION FUTURA de bahia_theme_reactive_icons.css - si no se bumpea, el
# browser/Cloudflare puede seguir sirviendo una copia vieja indefinidamente
# aunque el archivo en el servidor ya este actualizado (esto fue la causa raiz
# mas probable de que el fix de color reactivo de iconos de Autos/Citas
# Taller/Taller no se viera pese a estar bien desplegado en ambos
# contenedores - ver nota de investigacion completa en el propio .css).
app_include_css = ["/assets/bahia_theme/css/bahia_theme_reactive_icons.css?v=2"]

# Fix de condicion de carrera de swift_theme.api.boot.set_user_pref (ver
# swift_theme_race_fix.js para el detalle completo). Serializa esas llamadas
# puntuales sin tocar el codigo vendoreado de swift_theme.
app_include_js = ["/assets/bahia_theme/js/swift_theme_race_fix.js"]

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
	# Desktop Icon estandar de erpnext/frappe/hrms puestos en hidden=1 a mano
	# (2026-10-01, tras el bench migrate de la instalacion de swift_theme que
	# reseteo hidden=0 en 41 de ellos sin que nadie lo pidiera). Filtrado por
	# standard+app en vez de listar nombres a mano para que capture el set
	# completo (45: los 41 reseteados + los 4 que ya estaban ocultos antes:
	# CRM/Home/ERPNext/Support) sin tener que mantener la lista si cambia.
	# Prefijo "standard_hidden" para no pisar el archivo de arriba (mismo
	# doctype, filtro distinto -> archivo .json distinto, ver fixtures.py:
	# el nombre de archivo sale de dt+prefix, no hay merge entre entradas).
	{
		"dt": "Desktop Icon",
		"filters": [["standard", "=", 1], ["app", "in", ["erpnext", "frappe", "hrms"]]],
		"prefix": "standard_hidden",
	},
	# Workspace estandar de erpnext/frappe/hrms puestos en is_hidden=1 a mano
	# (2026-10-01, mismo incidente que los Desktop Icon de arriba pero en la
	# pagina "Home" de Workspaces, que es un mecanismo de visibilidad distinto
	# e independiente de Desktop Icon.hidden). Filtro por is_hidden=1 + app in
	# erpnext/frappe/hrms en vez de listar los 26 nombres a mano: Workspace
	# tiene el mismo campo "app" que Desktop Icon, y da exactamente ese set de
	# 26 sin tocar "Home"/"Welcome Workspace" (quedan is_hidden=0, se excluyen
	# solos) ni los 3 modulos custom (app=None). Mismo prefijo "standard_hidden"
	# que Desktop Icon para no pisar el fixture de arriba de los 3 Workspace
	# custom (archivo .json distinto por el prefix).
	{
		"dt": "Workspace",
		"filters": [["is_hidden", "=", 1], ["app", "in", ["erpnext", "frappe", "hrms"]]],
		"prefix": "standard_hidden",
	},
	# Role de solo lectura para integraciones (bot.comparador@bahiamotors.com)
	{"dt": "Role", "filters": [["name", "in", ["Comparador Solo Lectura"]]]},
	{"dt": "Custom DocPerm", "filters": [["role", "=", "Comparador Solo Lectura"]]},
	{"dt": "User", "filters": [["name", "in", ["bot.comparador@bahiamotors.com"]]]},
	# Permiso de lectura de Branch para System Manager (2026-10-02): Branch solo
	# traia permiso estandar para HR User/HR Manager, pero Citas/Autos/Taller
	# usan Branch como Link de Sucursal y el rol real usado para acceder a esos
	# modulos custom es System Manager (ver permisos de Cita de Taller/Vehiculo
	# arriba) - sin esto, cualquier usuario sin rol de HR ve "Permiso
	# insuficiente para Branch" al abrir la lista de Citas.
	{"dt": "Custom DocPerm", "filters": [["parent", "=", "Branch"], ["role", "=", "System Manager"]], "prefix": "branch_system_manager"},
	# Acceso de System Manager al reporte estandar "Delivery Note Trends"
	# ("Evolucion de las notas de entrega", 2026-10-02): el reporte viene
	# restringido de fabrica a Sales User/Stock Manager/Stock User/Accounts
	# User (su propia lista de roles en el child table "roles" del DocType
	# Report, independiente del DocPerm de Delivery Note) - el usuario real
	# tiene Sales Manager+System Manager, ninguno de los 4, y veia "Usted no
	# tiene acceso al Reporte". No se puede agregar via doc.save() normal
	# (Report.validate_standard_report() tira "Standard reports can only be
	# created in developer mode" para cualquier reporte estandar) - se
	# inserto el child row directo por API (sin pasar por el validate del
	# padre), igual que un Custom DocPerm nuevo.
	{"dt": "Has Role", "filters": [["parent", "=", "Delivery Note Trends"], ["parenttype", "=", "Report"], ["role", "=", "System Manager"]], "prefix": "delivery_note_trends_system_manager"},
]
