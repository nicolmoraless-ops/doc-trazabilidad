# Ejemplo Python Flask: documentación y trazabilidad

Proyecto de la actividad 3.4.2 (OCY1102). Una app Flask mínima cuyo pipeline de
Jenkins compila, prueba, genera documentación con Doxygen, versiona esa
documentación en Git y despliega la app en un entorno de prueba.

## Estructura

| Archivo | Para qué sirve |
|---|---|
| `app.py` | Aplicación Flask con comentarios Doxygen |
| `tests/test_app.py` | Pruebas unitarias (pytest) |
| `Doxyfile` | Configuración de Doxygen |
| `Jenkinsfile` | Pipeline: Build, Test, Generate Documentation, Version Control, Deploy |
| `scripts/doc_report.py` | Informe de cobertura de documentación y trazabilidad |
| `jenkins/` | Imagen de Jenkins con Python y Doxygen + docker-compose |
| `CHANGELOG.md` | Registro de cambios |

## Manual de instalación (local)

```
python -m venv venv
venv/bin/pip install -r requirements.txt      # Windows: venv\Scripts\pip
venv/bin/python -m pytest -v
venv/bin/python app.py                         # http://127.0.0.1:5000/hello?name=Duoc
```

## Manual de configuración

| Variable | Valor por defecto | Uso |
|---|---|---|
| `APP_HOST` | `127.0.0.1` | Interfaz donde escucha la app |
| `APP_PORT` | `5000` | Puerto |
| `FLASK_DEBUG` | `0` | `1` activa el modo debug (solo desarrollo) |

## Registro de dependencias

- flask 3.0.3
- pytest 8.3.3
- Doxygen (instalado en la imagen de Jenkins)
