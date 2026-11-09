# Changelog

Formato basado en Keep a Changelog. Versionado semántico.

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
