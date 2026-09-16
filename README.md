### Bahia Theme

Tema visual corporativo (colores de marca) para el Desk de ERPNext en Bahia Motors.

Esta app no agrega DocTypes ni lógica de negocio: su único propósito es inyectar
una hoja de estilos (`bahia_theme/public/css/bahia_theme.css`) vía el hook
`app_include_css` para aplicar los colores de marca de Bahía sobre elementos
puntuales del Desk (switcher de módulos, fondo del escritorio), sin tocar
archivos core de `frappe` ni de `erpnext`.

Ver comentarios dentro de `bahia_theme.css` para el detalle de cada selector
y por qué se eligió.

#### License

mit
