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
#
# v=3 (7-oct-2026): se agregaron las reglas de "Selling"/"ERPNext Settings"
# (2 iconos ESTANDAR de erpnext recien reactivados, ver fixture
# standard_hidden_desktop_icon.json) - mismo bump de cache-busting manual que
# ya hizo falta antes, por el mismo motivo documentado arriba (el path ya
# empieza con "/assets" asi que nunca pasa por el hash automatico de
# assets.json).
#
# v=4 (8-oct-2026): se agregaron las reglas de "Clientes" (icon=users) y
# "Proveedores" (icon=truck), 2 modulos custom nuevos - glyphs recortados a
# mano desde el sprite Lucide de frappe (ver nota de extension 8-oct-2026 en
# el propio .css para el detalle de por que Lucide necesito recorte manual
# igual que Autos/Citas Taller/Taller, a diferencia de Selling/ERPNext
# Settings). Mismo bump de cache-busting manual, mismo motivo.
#
# bahia_theme_datatable_header_fix.css (10-oct-2026): override puntual de 1
# regla de swift_theme (header de grilla/Vista de Reporte con fondo blanco en
# columnas que solo se ven al hacer scroll horizontal - ver el propio .css
# para el detalle completo de la causa). Archivo separado del de iconos
# (preocupaciones distintas), mismo mecanismo de cache-busting manual "?v=N"
# (ver nota de arriba de por que no sirve el hash automatico de assets.json).
#
# v=5 (11-oct-2026): se agrego la regla de "Requisiciones" (icon=
# clipboard-list), modulo custom nuevo - mismo recorte manual desde Lucide
# que Clientes/Proveedores. Mismo bump de cache-busting manual, mismo motivo.
app_include_css = [
	"/assets/bahia_theme/css/bahia_theme_reactive_icons.css?v=5",
	"/assets/bahia_theme/css/bahia_theme_datatable_header_fix.css?v=2",
]

# Fix de condicion de carrera de swift_theme.api.boot.set_user_pref (ver
# swift_theme_race_fix.js para el detalle completo). Serializa esas llamadas
# puntuales sin tocar el codigo vendoreado de swift_theme.
#
# Fix del redirect de sidebar a "Clientes" al refrescar sobre un DocType
# compartido entre modulos (ver bahia_theme_sidebar_module_fix.js para el
# detalle completo de la causa raiz real, confirmada 8-oct-2026 leyendo
# frappe/public/js/frappe/ui/sidebar/sidebar.js + boot.py::get_sidebar_items()).
app_include_js = [
	"/assets/bahia_theme/js/swift_theme_race_fix.js",
	"/assets/bahia_theme/js/bahia_theme_sidebar_module_fix.js",
]

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
	# Client Script del wizard "Nueva Cita de Taller" (2026-10-01, v3
	# 2026-10-12) - reemplaza el "+ Agregar" estandar de "Cita de Taller".
	# El modulo Python que consume (bahia_theme/api.py) NO es un DocType,
	# asi que no requiere developer_mode ni fixture propio - viaja con el
	# codigo del app en el repo.
	{"dt": "Client Script", "filters": [["name", "in", ["Cita de Taller Wizard Nuevo"]]]},
	# Property Setter puntuales creados a mano sobre DocTypes estandar/custom
	# (only_select en el Link "cliente" de Cita de Taller, 2026-10-11; y
	# show_title_field_in_link en Customer para que las columnas Link de
	# listas/reportes muestren el nombre real del cliente en vez del
	# codigo ciacod-dgcxccod, 2026-10-12). Filtrado por name exacto, no por
	# doc_type, porque Customer/Cita de Taller ya tienen muchos otros
	# Property Setter (in_list_view, naming_series, etc.) que NO son
	# nuestros y no deben quedar pisados/duplicados en este fixture.
	{"dt": "Property Setter", "filters": [["name", "in", ["Cita de Taller-cliente-only_select", "Customer-main-show_title_field_in_link"]]]},
	# Modulos custom migrados de GeneXus (shell Workspace + sidebar + tile)
	{"dt": "Workspace", "filters": [["name", "in", ["Autos", "Citas Taller", "Taller", "Clientes", "Proveedores", "Requisiciones"]]]},
	{"dt": "Workspace Sidebar", "filters": [["name", "in", ["Autos", "Citas Taller", "Taller", "Clientes", "Proveedores", "Requisiciones"]]]},
	{"dt": "Desktop Icon", "filters": [["name", "in", ["Autos", "Citas Taller", "Taller", "Clientes", "Proveedores", "Requisiciones"]]]},
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
	# Permiso de lectura de Warehouse para System Manager (2026-10-02): mismo
	# patron que Branch arriba - Warehouse solo traia permiso estandar para
	# Accounts User/Stock User/Sales User/Item Manager/Purchase User/
	# Manufacturing User, ninguno de los roles reales del usuario (Sales
	# Manager+System Manager) - "Permiso insuficiente para Warehouse" al
	# abrir cualquier pantalla que lo referencia como Link (ej. reportes de
	# stock/notas de entrega).
	{"dt": "Custom DocPerm", "filters": [["parent", "=", "Warehouse"], ["role", "=", "System Manager"]], "prefix": "warehouse_system_manager"},
	# Permiso de lectura de Serial No para System Manager (2026-10-02): mismo
	# patron que Branch/Warehouse arriba (solo traia Item Manager/Stock
	# Manager/Stock User de fabrica).
	{"dt": "Custom DocPerm", "filters": [["parent", "=", "Serial No"], ["role", "=", "System Manager"]], "prefix": "serial_no_system_manager"},
	# Dashboard "Citas Taller" (11-oct-2026): reemplaza el placeholder del
	# sidebar `DBCitas`/Dashboard (ver migracion-erpnext/citas.md, Menu real
	# §1 "DBCitas ... RESUELTO"). 100% nativo de ERPNext (Dashboard +
	# Dashboard Chart), sin codigo custom - igual de vulnerable a perderse en
	# un rebuild que los Workspace/Desktop Icon de arriba si no queda
	# declarado como fixture.
	{"dt": "Dashboard", "filters": [["name", "in", ["Citas Taller"]]]},
	{
		"dt": "Dashboard Chart",
		"filters": [[
			"name", "in", [
				"Citas Taller - Conteo por Fecha",
				"Citas Taller - Estados (Taller)",
				"Citas Taller - Estados (Express-Combo)",
			],
		]],
	},
	# DocType custom "Configuracion Api" (11-oct-2026): reemplaza el
	# placeholder del sidebar `VECONFIGURACIONAPI`/"Configuración de Apis"
	# (ver migracion-erpnext/citas.md). El Custom DocPerm de solo lectura
	# para "Comparador Solo Lectura" ya queda cubierto por el filtro generico
	# de ese rol mas arriba (linea ~194), no hace falta una entrada aparte.
	# OJO: "DocType" NO se puede declarar como fixture sin developer_mode
	# ("Cannot export DocType doctype as a fixture, since it can only be
	# created in developer mode from desk" - confirmado al intentarlo acá).
	# Este servidor corre con developer_mode=null a proposito (ver reglas del
	# proyecto), asi que la definicion de "Configuracion Api" (campos,
	# permisos) NO queda protegida por este mecanismo de fixtures - mismo
	# riesgo de perdida en un rebuild/migrate que ya genero el incidente del
	# 16-sep-2026 con los primeros Workspace custom, sin mitigacion
	# disponible por esta via. Pendiente de decision del coordinador (unica
	# alternativa real: activar developer_mode, lo cual tiene sus propias
	# implicancias que no se evaluaron en esta pasada).
	# Dashboard "Citas Ocupación" (11-oct-2026): reemplaza el placeholder del
	# sidebar `CitasOcupacion` (categoria "Dashboard" del sidebar de GeneXus,
	# ver migracion-erpnext/citas.md, Menu real §Actualizacion 2026-10-11).
	# GX usa un objeto tipo `Dashboard` nativo (no `Query`, tipo no soportado
	# por las tools de investigacion disponibles) que muestra ocupacion del
	# mes actual con una regla de gracia (antes del dia 4 usa el mes
	# anterior) - no replicable 1:1 con los filtros nativos de Dashboard
	# Chart. Se aproximo con 2 charts sobre "Cita de Taller" con
	# timespan="Last Month" (ventana rodante de 1 mes hacia atras desde hoy,
	# NO el mes calendario con la regla de gracia del original - ver
	# frappe/utils/dateutils.py::get_from_date_from_timespan). Documentado
	# como aproximacion, no como replica exacta.
	# prefix obligatorio: sin el, pisa dashboard.json/dashboard_chart.json de
	# "Citas Taller" de arriba (mismo dt sin prefix -> mismo nombre de archivo,
	# sin merge entre entradas - confirmado en vivo: la primera corrida de
	# export-fixtures sin este prefix borro Citas Taller del fixture, corregido
	# en la misma sesion).
	{"dt": "Dashboard", "filters": [["name", "in", ["Citas Ocupación"]]], "prefix": "citas_ocupacion"},
	{
		"dt": "Dashboard Chart",
		"filters": [[
			"name", "in", [
				"Citas Ocupación - Conteo Diario",
				"Citas Ocupación - Estados",
			],
		]],
		"prefix": "citas_ocupacion",
	},
]
