from flask import Blueprint, jsonify
import app.controllers.historia_controllers as controller

historia_bp = Blueprint('historias', __name__, url_prefix='/historias')

@historia_bp.route('/', methods=['GET'])
def listar():
    try:
        historias = controller.listar()
        return jsonify(historias), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
