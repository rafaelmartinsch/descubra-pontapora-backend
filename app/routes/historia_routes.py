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
    
@historia_bp.route('/<int:id>', methods=['GET'])
def buscar_historia(id):
    try:
        historias = controller.buscar_por_id(id)
        if historias:
            return jsonify(historias), 200
        return jsonify({"mensagem": "Historia não encontrado"}), 404
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
