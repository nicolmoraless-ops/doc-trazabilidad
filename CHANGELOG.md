# Changelog

Formato basado en Keep a Changelog. Versionado semántico.

## [1.1.1]
### Corregido
- Docstring de `/hello`: `@param name` provocaba una advertencia de Doxygen porque `name` es un parámetro de la URL, no de la función (detectado por el build #1).
- Stage Version Control: la doc se arma en una carpeta temporal en vez del workspace (el build #2 falló porque quedaba la rama `docs-tmp` del build #1) y la rama `docs` ahora conserva el historial de cada build.
- Las notificaciones por correo ya no marcan el build como FAILURE si no hay servidor SMTP; la alerta queda siempre en la consola.

## [1.1.0]
### Añadido
- Jenkinsfile con stages Build, Test, Generate Documentation, Version Control y Deploy.
- `scripts/doc_report.py`: cobertura de docstrings, advertencias de Doxygen y datos de trazabilidad (commit, autor, build).
- Endpoint `/health` para la verificación del despliegue.
- Pruebas unitarias con pytest.
### Seguridad
- `/hello` escapa el parámetro `name` (evita XSS reflejado).
- `debug=True` eliminado; el modo debug ahora depende de `FLASK_DEBUG`.

## [1.0.0]
### Añadido
- App Flask de ejemplo con endpoint `/hello` y Doxyfile inicial.
