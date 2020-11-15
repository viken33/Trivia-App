# app/errors/routes.py

from . import errors_bp
from flask import render_template, jsonify
from werkzeug.exceptions import HTTPException

""" manejo de errores """
# Se envia un template especifico por cada error
# Se incluye el error capturado aunque se deja con el texto por defecto


@errors_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=str(e)), 404


@errors_bp.app_errorhandler(401)
def unathorized(e):
    return render_template('401.html', error=str(e)), 401


@errors_bp.app_errorhandler(HTTPException)
def handle_exception(e):
    return render_template('500.html', error=str(e)), 500

""" # Ruta de prueba para los codigos de error
@errors_bp.route('/test')
def test_principal():
    abort(500)  """


