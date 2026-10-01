// Fix para una condicion de carrera real de swift_theme (confirmada contra
// logs de acceso de nginx reales el 2026-10-01): al elegir un preset de color
// o colores custom, swift-boot.js dispara 3 POST en paralelo contra
// swift_theme.api.boot.set_user_pref (swift_preset / swift_primary /
// swift_secondary), las 3 pegandole a la misma fila de `tabUser`. Bajo esa
// concurrencia, 1 o 2 de las 3 vuelven intermitentemente con 500 (tamaño de
// respuesta identico en todos los casos: 2914 bytes). swift_density nunca
// falla porque esa se manda sola, nunca en paralelo con otra.
//
// No se toca el codigo vendoreado de swift_theme (apps/swift_theme) para que
// el fix sobreviva a un futuro `bench update` de esa app - en cambio, se
// intercepta frappe.call() globalmente desde acá y se encolan (serializan)
// específicamente las llamadas a este método, sin tocar ninguna otra.
(function () {
	if (!window.frappe || frappe.call.__bahia_swift_race_fix__) return;

	var TARGET_METHOD = "swift_theme.api.boot.set_user_pref";
	var _origCall = frappe.call.bind(frappe);
	var _queue = Promise.resolve();

	function patchedCall(opts) {
		if (!opts || opts.method !== TARGET_METHOD) {
			return _origCall(opts);
		}

		return new Promise(function (resolve) {
			_queue = _queue.then(function () {
				return new Promise(function (settleQueueStep) {
					var userCallback = opts.callback;
					var userAlways = opts.always;
					var userError = opts.error;

					_origCall(
						Object.assign({}, opts, {
							callback: function (r) {
								if (userCallback) userCallback(r);
								resolve(r);
							},
							error: function (r) {
								if (userError) userError(r);
								resolve(r);
							},
							always: function (r) {
								if (userAlways) userAlways(r);
								settleQueueStep();
							},
						})
					);
				});
			});
		});
	}

	patchedCall.__bahia_swift_race_fix__ = true;
	frappe.call = patchedCall;
})();
