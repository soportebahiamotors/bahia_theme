import json

import frappe
from frappe import _
from frappe.utils import cint, getdate


# ---------------------------------------------------------------------------
# Wizard "Nueva Cita de Taller" - ver migracion-erpnext/citas.md seccion
# "Menu real (gxmenu-specialist)" -> "Flujo real de alta/agendamiento de una
# Cita" (reescrita 2026-10-01) para el detalle linea por linea de cada
# control real de GeneXus (CitasExww / Citassd) que este modulo replica.
#
# v3 (2026-10-12): correcciones de "## Modelo de datos" seccion 12.D sobre la
# re-verificacion directa del wizard real contra la KB viva - buscador de 3
# campos (Placa/Chasis, Cliente, RUC/Cedula, antes solo Placa), filtro de
# vehiculo solo Vendido, y bloqueo real de cliente inactivo.
# ---------------------------------------------------------------------------

CUSTOMER_PHONE_FIELDS = [
	("celular", "Celular"),
	("telefono", "Telefono"),
	("telefono_oficina", "Telefono Oficina"),
	("telefono2", "Telefono 2"),
]

# Buckets de cupo replicados en el widget del Paso 2. Ver citas.md "Reglas de
# negocio" #6 y "Menu real" #0: el esquema fisico real de
# CitasCuposConfiguracion (18 columnas, confirmado contra el DWH) tiene
# semana/fin-de-semana por tipo. Domingo = 0 cupos siempre (regla hardcodeada
# en GeneXus, Citas010 - DayOfWeek()=1). Sabado se trata igual que domingo a
# los efectos de elegir semana/finde (mismo criterio de
# ComboHorasCitas/CitasBahiasDisponiblesFechaHora: DayOfWeek()=7 => finde).
BUCKETS = ("taller", "movil", "express_adicional", "taller_adicional")

BUCKET_LABELS = {
	"taller": "Mant. / Taller",
	"movil": "Movil",
	"express_adicional": "Express Adicional",
	"taller_adicional": "Taller Adicional",
}


def _armar_ficha_vehiculo(veh):
	"""Arma la ficha de referencia (Paso 1) a partir de una fila de Vehiculo
	ya leida (dict con los campos de _VEHICULO_FIELDS). Replica CitasExww
	(ficha mostrada al elegir un vehiculo) - NO incluye "proximo
	mantenimiento" (REST externo `getRest_consultamantenimiento`, no migrado,
	fuera de alcance explicito, ver citas.md)."""
	cliente = None
	if veh.get("ciacod") and veh.get("cliente_cxc"):
		cliente = frappe.db.get_value(
			"Customer",
			{"ciacod_origen": veh["ciacod"], "codigo_origen": veh["cliente_cxc"]},
			[
				"name",
				"customer_name",
				"tax_id",
				"email_id",
				"email_datgencxc",
				"celular",
				"telefono",
				"telefono2",
				"telefono_oficina",
				"direccion",
				"direccion_oficina",
				"disabled",
			],
			as_dict=True,
		)

	descripcion = " ".join(filter(None, [veh.get("brand"), veh.get("modelo"), veh.get("version")])) or None

	pendientes = frappe.get_all(
		"Cita de Taller",
		filters={
			"vehiculo": veh["name"],
			"estado": ["not in", ["Cancelada", "Facturada"]],
		},
		fields=["name", "fecha_cita", "hora_cita", "estado", "origen_canal_cita"],
		order_by="fecha_cita desc",
		limit=5,
	)

	telefonos = []
	if cliente:
		for fieldname, label in CUSTOMER_PHONE_FIELDS:
			valor = cliente.get(fieldname)
			if valor:
				telefonos.append({"label": label, "valor": valor})

	return {
		"vehiculo": veh["name"],
		"placa": veh.get("placa"),
		"vin": veh.get("vin"),
		"anio": veh.get("anio"),
		"marca": veh.get("brand"),
		"modelo": veh.get("modelo"),
		"version": veh.get("version"),
		"color": veh.get("color_exterior"),
		"descripcion": descripcion,
		"estado_comercial": veh.get("estado_comercial"),
		"ciacod": veh.get("ciacod"),
		"company": veh.get("company"),
		"cliente": cliente.name if cliente else None,
		"cliente_nombre": cliente.customer_name if cliente else None,
		"cliente_ruc": cliente.tax_id if cliente else None,
		"cliente_email": (cliente.email_id or cliente.email_datgencxc) if cliente else None,
		"cliente_direccion": (cliente.direccion or cliente.direccion_oficina) if cliente else None,
		"cliente_disabled": bool(cliente.disabled) if cliente else False,
		"telefonos": telefonos,
		"citas_pendientes": pendientes,
	}


_VEHICULO_FIELDS = [
	"name",
	"placa",
	"vin",
	"anio",
	"ciacod",
	"company",
	"brand",
	"modelo",
	"version",
	"color_exterior",
	"color_interior",
	"estado_comercial",
	"cliente_cxc",
]


@frappe.whitelist()
def buscar_vehiculo_placa(placa=None, cliente_nombre=None, ruc=None):
	"""Paso 1 del wizard: busca Vehiculo por Placa/Chasis, por nombre de
	Cliente, o por RUC/Cedula (los 3 combinables, con OR entre los que vengan
	con valor). Replica los 3 campos reales decodificados del `webform` de
	`CitasExww` (`&GenericFilter_Grid`, `&fDgCxcNombre`, `&fDgCxcRuc` - ver
	citas.md seccion 12.A) - antes este buscador solo tenia 1 campo (Placa).

	Solo vehiculos ya `Vendido` aparecen (replica el filtro real
	`VehStatus in (Vendido, Flota)` de GeneXus - en este dataset no existe
	ningun vehiculo con estado_comercial='Flota', se filtra solo por
	'Vendido'; un auto en stock sin vender nunca aparece en este buscador,
	igual que en GX)."""
	placa = (placa or "").strip()
	cliente_nombre = (cliente_nombre or "").strip()
	ruc = (ruc or "").strip()

	if not placa and not cliente_nombre and not ruc:
		frappe.throw(_("Ingrese Placa/Chasis, Cliente o RUC/Cedula"))

	conditions = ["v.estado_comercial = 'Vendido'"]
	values = {}
	or_parts = []
	if placa:
		or_parts.append("(v.placa = %(placa_exact)s OR v.placa LIKE %(placa_like)s OR v.vin LIKE %(placa_like)s)")
		values["placa_exact"] = placa
		values["placa_like"] = f"{placa}%"
	if cliente_nombre:
		or_parts.append("c.customer_name LIKE %(cliente_like)s")
		values["cliente_like"] = f"%{cliente_nombre}%"
	if ruc:
		or_parts.append("c.tax_id LIKE %(ruc_like)s")
		values["ruc_like"] = f"{ruc}%"
	conditions.append("(" + " OR ".join(or_parts) + ")")

	rows = frappe.db.sql(
		f"""
		SELECT v.name FROM tabVehiculo v
		LEFT JOIN tabCustomer c
			ON c.ciacod_origen = v.ciacod AND c.codigo_origen = v.cliente_cxc
		WHERE {" AND ".join(conditions)}
		ORDER BY v.modified DESC
		LIMIT 10
		""",
		values,
		as_dict=True,
	)
	if not rows:
		return []

	orden = [r.name for r in rows]
	vehiculos = frappe.get_all(
		"Vehiculo",
		filters={"name": ["in", orden]},
		fields=_VEHICULO_FIELDS,
	)
	vehiculos.sort(key=lambda v: orden.index(v["name"]))
	return [_armar_ficha_vehiculo(v) for v in vehiculos]


@frappe.whitelist()
def ficha_vehiculo(vehiculo):
	"""Variante de buscar_vehiculo_placa que resuelve por Vehiculo.name
	directo (selector "avanzado" de codigo interno del wizard)."""
	if not vehiculo:
		frappe.throw(_("Vehiculo requerido"))
	veh = frappe.db.get_value("Vehiculo", vehiculo, _VEHICULO_FIELDS, as_dict=True)
	if not veh:
		frappe.throw(_("Vehiculo {0} no encontrado").format(vehiculo))
	return _armar_ficha_vehiculo(veh)


def _len_json_list(valor):
	if not valor:
		return 0
	try:
		parsed = json.loads(valor)
	except Exception:
		return 0
	return len(parsed) if isinstance(parsed, list) else 0


@frappe.whitelist()
def cupos_disponibles(sucursal, fecha):
	"""Widget de cupos en tiempo real (Paso 2): cupo configurado vs. usado
	para una Sucursal+Fecha, por tipo (Mant./Taller, Movil, Express
	Adicional, Taller Adicional). Cruza `Cupos por Sucursal`/`Cupos por
	Sucursal Detalle` (18 columnas reales) contra `Cita de Taller` ya
	existentes para esa sucursal+fecha, excluyendo Reprogramada/Cancelada
	(mismo criterio confirmado para `CitasBahiasDisponiblesFechaHora` en
	GeneXus). Ver citas.md "Reglas de negocio" #6 y "Menu real" #0/#1.

	Limitacion documentada (ver citas.md): el mapeo exacto entre
	`origen_canal_cita`+`cita_adicional` y cada uno de los 4 buckets de cupo
	es una inferencia razonable, no confirmada 100% contra codigo fuente GX
	para el esquema fisico real (desfasaje KB-vs-produccion ya documentado) -
	tratar "usados" como aproximado, no como fuente de verdad absoluta.

	Este metodo en si mismo no bloquea nada (sigue siendo solo una consulta) -
	el BLOQUEO real (replicando el comportamiento confirmado de `Sub
	'U_Confirmar'` de Citassd, ver citas.md seccion 12.B.4) vive del lado del
	Client Script (`Cita de Taller Wizard Nuevo`), que impide enviar el
	formulario si el bucket calculado esta en 0 y el usuario no tildo "Cita
	Adicional" - no hay revalidacion atomica server-side de concurrencia
	(mismo alcance que GeneXus: el gate es de interfaz, no de Rules).
	"""
	if not sucursal or not fecha:
		return {}

	fecha = getdate(fecha)
	es_domingo = fecha.weekday() == 6  # Python: Monday=0 .. Sunday=6
	es_finde = fecha.weekday() in (5, 6)  # sabado o domingo

	cupos_doc = frappe.db.get_value("Cupos por Sucursal", {"sucursal": sucursal}, "name")
	if not cupos_doc:
		return {"sin_configuracion": True}

	if es_domingo:
		configurado = {b: 0 for b in BUCKETS}
	else:
		sufijo = "finde" if es_finde else "semana"
		detalle = frappe.get_all(
			"Cupos por Sucursal Detalle",
			filters={"parent": cupos_doc},
			fields=[
				f"cupo_taller_{sufijo}",
				f"bahias_movil_{sufijo}",
				f"adicionales_express_{sufijo}",
				f"adicionales_taller_{sufijo}",
			],
		)
		configurado = {b: 0 for b in BUCKETS}
		for fila in detalle:
			configurado["taller"] += cint(fila.get(f"cupo_taller_{sufijo}"))
			configurado["movil"] += _len_json_list(fila.get(f"bahias_movil_{sufijo}"))
			configurado["express_adicional"] += _len_json_list(fila.get(f"adicionales_express_{sufijo}"))
			configurado["taller_adicional"] += cint(fila.get(f"adicionales_taller_{sufijo}"))

	citas_del_dia = frappe.get_all(
		"Cita de Taller",
		filters={
			"sucursal": sucursal,
			"fecha_cita": fecha,
			"estado": ["not in", ["Reprogramada", "Cancelada"]],
		},
		fields=["origen_canal_cita", "cita_adicional"],
	)

	usados = {b: 0 for b in BUCKETS}
	for c in citas_del_dia:
		adicional = cint(c.cita_adicional)
		origen = c.origen_canal_cita or ""
		if origen.startswith("Reparacion"):
			usados["taller_adicional" if adicional else "taller"] += 1
		elif origen.startswith("Movil"):
			usados["movil"] += 1
		elif adicional:
			# Mantenimiento (E) / Mant. Plus (P) / Diagnostico (D) con
			# cita_adicional=1. Sin "adicional" no hay bucket numerico
			# confirmado contra el esquema fisico real para estos 3 origenes
			# (ver citas.md) - no se cuentan contra ningun bucket.
			usados["express_adicional"] += 1

	return {
		"es_domingo": es_domingo,
		"es_finde": es_finde,
		"buckets": {
			b: {
				"configurado": configurado[b],
				"usados": usados[b],
				"disponibles": max(configurado[b] - usados[b], 0),
				"label": BUCKET_LABELS[b],
			}
			for b in BUCKETS
		},
	}


@frappe.whitelist()
def crear_cita_taller(
	vehiculo,
	origen_canal_cita,
	sucursal=None,
	bahia=None,
	fecha_cita=None,
	hora_cita=None,
	turno="Diurno",
	confirmacion=0,
	cita_adicional=0,
	dos_espacios=0,
	tiempo_aproximado_horas=None,
	observaciones_cliente=None,
	cliente=None,
	servicios=None,
):
	"""Crea una 'Cita de Taller' desde el wizard de 2 pasos (Client Script
	'Cita de Taller Wizard Nuevo'), generando ciacod_origen/codigo_origen
	internamente - el usuario nunca los ve ni los tipea.

	No revalida el cupo en el servidor (el bloqueo de cupo=0 vive en el Client
	Script, igual que en GeneXus - ver docstring de `cupos_disponibles`): esta
	funcion confia en que el cliente ya hizo ese chequeo. Si se llama
	directo (ej. API/consola) con cupo en 0, SI crea la cita sin bloqueo -
	mismo alcance que GeneXus (sin `Error()` server-side en las Rules de
	`Citas`/`CITASCOMBOS`).

	Numeracion interna SIMPLE (no replica el numerador real de GeneXus
	ULT_Numeradores/tabla Numeradores - no hace falta para este alcance,
	ver bitacora migracion-erpnext/citas.md seccion 'Reglas de negocio' #4):
	MAX(codigo_origen numerico) ya usado para esa compania + 1, con un par
	de reintentos si choca contra el autoname (poco probable, uso interno
	de baja concurrencia).
	"""
	if not vehiculo:
		frappe.throw(_("Debe seleccionar un vehiculo"))
	if not origen_canal_cita:
		frappe.throw(_("Debe seleccionar el tipo de cita"))

	veh = frappe.db.get_value(
		"Vehiculo",
		vehiculo,
		["ciacod", "company", "cliente_cxc", "placa", "modelo"],
		as_dict=True,
	)
	if not veh:
		frappe.throw(_("Vehiculo {0} no encontrado").format(vehiculo))

	ciacod_origen = veh.ciacod
	if not ciacod_origen:
		frappe.throw(_("El vehiculo {0} no tiene CiaCod de origen (ciacod) definido").format(vehiculo))

	cliente_resuelto = cliente
	if not cliente_resuelto and veh.cliente_cxc:
		cliente_resuelto = frappe.db.get_value(
			"Customer",
			{"ciacod_origen": ciacod_origen, "codigo_origen": veh.cliente_cxc},
			"name",
		)

	if cliente_resuelto and frappe.db.get_value("Customer", cliente_resuelto, "disabled"):
		# Replica el bloqueo real de GeneXus (Event 'Seleccionar' de CitasExww,
		# ver citas.md seccion 12.A) - mismo mensaje exacto. El wizard ya
		# bloquea esto en el Paso 1 (cliente), esto es defensa en profundidad
		# server-side por si se llega aca por otra via (ej. API directa).
		frappe.throw(_("No se permite crear citas para autos asociados a clientes inactivos."))

	bahia_valor = None
	if bahia:
		# `Cita de Taller.bahia` es un campo Data (no Link) - se guarda el
		# numero de bahia (equivalente a `CCNumBahia`/`BahiaSucNum` en
		# GeneXus), no el nombre interno del doc "Bahia de Sucursal".
		bahia_valor = frappe.db.get_value("Bahia de Sucursal", bahia, "numero_bahia")
		if bahia_valor is None:
			bahia_valor = bahia

	if isinstance(servicios, str):
		servicios = frappe.parse_json(servicios) if servicios else []
	servicios = servicios or []

	last_error = None
	for _intento in range(3):
		codigo_origen = _siguiente_codigo_origen(ciacod_origen)
		doc = frappe.new_doc("Cita de Taller")
		doc.origen_canal_cita = origen_canal_cita
		doc.empresa = veh.company
		doc.ciacod_origen = ciacod_origen
		doc.codigo_origen = codigo_origen
		doc.fecha_cita = fecha_cita
		doc.hora_cita = hora_cita
		doc.turno = turno or "Diurno"
		doc.confirmacion = 1 if cint(confirmacion) else 0
		doc.cita_adicional = 1 if cint(cita_adicional) else 0
		doc.estado = "Cita"
		doc.sucursal = sucursal
		doc.bahia = bahia_valor
		doc.cliente = cliente_resuelto
		doc.cliente_dgcxc_origen = veh.cliente_cxc
		doc.vehiculo = vehiculo
		doc.placa = veh.placa
		doc.modelo = veh.modelo
		doc.observaciones_cliente = observaciones_cliente
		doc.creado_por_origen = frappe.session.user
		doc.fecha_creacion_origen = frappe.utils.now_datetime()

		# Campos nuevos ("Dos espacios"/"Tiempo aproximado") solo si el
		# Custom Field ya fue aplicado en este sitio (ver
		# setup_cita_wizard_v2.py) - no revienta si todavia no corrio.
		if doc.meta.has_field("dos_espacios"):
			doc.dos_espacios = 1 if cint(dos_espacios) else 0
		if doc.meta.has_field("tiempo_aproximado_horas") and tiempo_aproximado_horas not in (None, ""):
			doc.tiempo_aproximado_horas = tiempo_aproximado_horas

		for s in servicios:
			if not isinstance(s, dict):
				continue
			if not (s.get("tipo_trabajo") or s.get("precio")):
				continue
			doc.append(
				"servicios_solicitados",
				{
					"tipo_trabajo": s.get("tipo_trabajo"),
					"trabajcod_origen": s.get("trabajcod_origen"),
					"factor": s.get("factor"),
					"unidad_tiempo": s.get("unidad_tiempo"),
					"precio": s.get("precio"),
				},
			)

		try:
			doc.insert()
			return doc.name
		except frappe.DuplicateEntryError as e:
			last_error = e
			continue

	frappe.throw(_("No se pudo generar un codigo interno unico para la cita, intente de nuevo. ({0})").format(last_error))


def _siguiente_codigo_origen(ciacod_origen):
	row = frappe.db.sql(
		"""
		SELECT COALESCE(MAX(CAST(codigo_origen AS UNSIGNED)), 0)
		FROM `tabCita de Taller`
		WHERE ciacod_origen=%s AND codigo_origen REGEXP '^[0-9]+$'
		""",
		(ciacod_origen,),
	)
	siguiente = frappe.utils.cint(row[0][0] if row else 0) + 1
	return str(siguiente)
