from flask import Blueprint, jsonify, request

import app.controllers.eventos_controllers as controller

eventos_bp = Blueprint('eventos', __name__, url_prefix='/eventos')

@eventos_bp.route('/', methods=['GET'])
def ordenados_por_data():
    try:
        eventos = controller.ordenados_por_data()
        return jsonify(eventos), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@eventos_bp.route('/', methods=['POST'])
def criar_evento():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados ausentes no corpo da requisição'}), 400

        novo_evento = controller.criar_evento(data)
        return jsonify(novo_evento), 201
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@eventos_bp.route('/<int:evento_id>', methods=['PUT'])
def atualizar_evento(evento_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'mensagem': 'Dados ausentes no corpo da requisição'}), 400

        evento_atualizado = controller.atualizar_evento(evento_id, data)
        if not evento_atualizado:
            return jsonify({'mensagem': 'Evento não encontrado'}), 404
            
        return jsonify(evento_atualizado), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@eventos_bp.route('/<int:evento_id>', methods=['DELETE'])
def deletar_evento(evento_id):
    try:
        success = controller.deletar_evento(evento_id)
        if not success:
            return jsonify({'mensagem': 'Evento não encontrado'}), 404
            
        return '', 204  # No Content
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500