from flask import Blueprint, jsonify
import app.controllers.eventos_controllers as controller

eventos_bp = Blueprint('eventos', __name__, url_prefix='/eventos')

@eventos_bp.route('/', methods=['GET'])
def ordenados_por_data():
    try:
        eventos = controller.ordenados_por_data()
        return jsonify(eventos), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
