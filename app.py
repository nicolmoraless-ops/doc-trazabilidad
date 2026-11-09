##
# @file app.py
# @brief Aplicación Flask de ejemplo documentada con Doxygen.
# @details Expone un endpoint /hello que saluda al usuario. Usada en la
#          actividad 3.4.2 para demostrar documentación y trazabilidad en CI/CD.
# @version 1.1.0
#
import os

from flask import Flask, request
from markupsafe import escape

## Instancia principal de la aplicación Flask.
app = Flask(__name__)


@app.route('/hello')
def hello():
    """!
    @brief Endpoint para saludar al usuario.

    @details Lee el parámetro de consulta "name" (nombre del usuario) desde
             la URL, por ejemplo /hello?name=Duoc. Si no viene, usa "Mundo".
             El valor se escapa para evitar XSS reflejado.

    @return str Mensaje de saludo.
    """
    name = request.args.get('name', 'Mundo')
    return f"Hello, {escape(name)}!"


@app.route('/health')
def health():
    """!
    @brief Endpoint de salud usado por el stage Deploy del pipeline.
    @return dict Estado del servicio.
    """
    return {"status": "ok"}


if __name__ == '__main__':
    # debug solo si se pide explícitamente (nunca en producción)
    app.run(host=os.getenv('APP_HOST', '127.0.0.1'),
            port=int(os.getenv('APP_PORT', '5000')),
            debug=os.getenv('FLASK_DEBUG', '0') == '1')
