// Fix para el bug real reportado 2026-10-08: al refrescar (F5) estando
// parado en un DocType compartido entre varios Workspace Sidebar (ej.
// "Pais"/"Provincia", creados para "Autos" pero tambien referenciados desde
// "Clientes"), Frappe cambia el sidebar izquierdo al Workspace equivocado
// ("Clientes" ganaba siempre).
//
// Causa raiz confirmada leyendo
// apps/frappe/frappe/public/js/frappe/ui/sidebar/sidebar.js (version real
// que corre en este servidor desde el rebuild de imagen del 16-sep-2026,
// NO es un archivo tocado por bahia_theme ni por swift_theme - swift-sidebar.js
// solo hace show/hide, no toca esta logica) +
// apps/frappe/frappe/boot.py::get_sidebar_items():
//
//   1. Sidebar.prototype.resolve_sidebar(entity, module) arma `candidates`
//      (todos los Workspace Sidebar que tienen un item con link_to==entity)
//      recorriendo `frappe.boot.workspace_sidebar_item` con Object.entries().
//   2. Ese objeto se arma en boot.py::get_sidebar_items() a partir de
//      frappe.get_all("Workspace Sidebar", ...) SIN order_by explicito -> usa
//      el sort_field/sort_order default del DocType "Workspace Sidebar", que
//      es creation DESC. Es decir: el Workspace Sidebar creado MAS
//      RECIENTEMENTE queda primero en el dict/objeto.
//   3. Cuando resolve_sidebar() no puede desambiguar por nombre de modulo
//      exacto (candidates.find(c => c.toLowerCase() === module?.toLowerCase())
//      no matchea nada), cae al fallback final: `sidebar_name = candidates[0]`
//      -> siempre gana el Workspace Sidebar creado mas recientemente entre
//      los que referencian ese DocType.
//   4. Sidebar.prototype.refresh() (se dispara en cada "page-change/form-
//      refresh", incluido un F5 real) llama a
//      `this.set_workspace_sidebar()` SIN pasarle el router -> adentro,
//      `const module = router?.meta?.module` queda `undefined` -> se pierde
//      la unica senal que hubiera permitido resolver por
//      `resolve_module_sidebar(module)` (que SI matchea si existe un
//      Workspace Sidebar con el mismo nombre que el modulo real del DocType,
//      ej. Pais/Provincia tienen DocType.module="Autos" y existe un sidebar
//      llamado "Autos").
//
// Como "Clientes" (creado 8-oct) es mas nuevo que "Autos"/"Taller"/"Citas
// Taller" (creados 16/17/19-sep), termina ganando el fallback para CUALQUIER
// DocType que tambien aparezca en el sidebar de Clientes (Pais, Provincia,
// Mode of Payment, Customer) cada vez que el modulo no se puede recuperar.
//
// Fix: NO se toca sidebar.js (ya es un archivo "no estandar"/fragil, sumarle
// mas parches directos lo hace peor y se pierde en el proximo rebuild de
// imagen sin dejar rastro). En cambio, se parchea SOLO
// `resolve_sidebar()` desde afuera (via app_include_js de bahia_theme, que
// SI sobrevive a un rebuild porque esta versionado en el repo de la app):
// si llega sin `module`, se lo recupera directo del meta del DocType de la
// ruta actual (`frappe.get_meta(doctype).module`) antes de delegar al
// metodo original. Esto no cambia NADA del comportamiento existente para el
// caso ya resuelto (module explicito) - solo recupera informacion que hoy
// se pierde en el camino de refresh().
//
// Alcance real confirmado por SQL contra esta instancia (2026-10-08):
// - Pais.module="Autos", Provincia.module="Autos" -> con este fix, refrescar
//   sobre esos 2 catalogos vuelve a resolver "Autos" (antes: "Clientes").
// - Customer.module="Selling" -> con este fix resuelve "Selling" (el
//   Workspace nativo de ERPNext que de verdad es dueño de Customer), no
//   "Clientes" - una mejora real aunque no sea "quedarse en Autos/Taller"
//   (ese caso de "recordar en que sidebar estaba el usuario" no se puede
//   resolver sin tocar sidebar.js mismo, ver nota en clientes.md).
// - Mode of Payment.module="Accounts" -> NO existe un Workspace Sidebar
//   literalmente llamado "Accounts" (existe "Accounts Setup"/"Invoicing"/
//   "Financial Reports") -> este caso puntual sigue sin resolverse por este
//   fix, cae al mismo fallback de siempre (hoy: "Clientes", por ser el mas
//   nuevo). Documentado como limite conocido, no bloqueante.
(function () {
	if (!window.frappe) return;

	function patch() {
		if (
			!frappe.ui ||
			!frappe.ui.Sidebar ||
			!frappe.ui.Sidebar.prototype ||
			frappe.ui.Sidebar.prototype.__bahia_resolve_sidebar_module_fix__
		) {
			return;
		}

		var original_resolve_sidebar = frappe.ui.Sidebar.prototype.resolve_sidebar;
		if (typeof original_resolve_sidebar !== "function") return;

		frappe.ui.Sidebar.prototype.resolve_sidebar = function (entity, module) {
			if (!module) {
				try {
					var route = frappe.get_route();
					var doctype = route && route[1];
					if (doctype) {
						var meta = frappe.get_meta(doctype);
						if (meta && meta.module) {
							module = meta.module;
						}
					}
				} catch (e) {
					// defensivo: si algo falla acá, se sigue con el comportamiento
					// original (module undefined), nunca se rompe la navegación.
				}
			}
			return original_resolve_sidebar.call(this, entity, module);
		};

		frappe.ui.Sidebar.prototype.__bahia_resolve_sidebar_module_fix__ = true;
	}

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", patch);
	} else {
		patch();
	}
	document.addEventListener("app_ready", patch);
	if (frappe.after_ajax) frappe.after_ajax(patch);
})();
