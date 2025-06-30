# app/routes/eventos_routs.py

from flask import Blueprint, jsonify, request
# Importa o controlador de eventos, não o de locais
import app.controllers.eventos_controllers as controller

eventos_bp = Blueprint('eventos', __name__, url_prefix='/eventos')

@eventos_bp.route('/', methods=['GET'])
def listar_eventos():
    """
    Rota para listar todos os eventos ordenados por data.
    Retorna uma lista de eventos em formato JSON.
    """
    try:
        eventos = controller.ordem_por_data()
        return jsonify(eventos), 200
    except Exception as e:
        # Em caso de erro, retorna uma mensagem de erro com status 500
        return jsonify({'mensagem': str(e)}), 500
