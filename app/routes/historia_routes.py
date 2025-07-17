from flask import Blueprint, request, jsonify
import app.controllers.historia_controllers as controller

historia_bp = Blueprint('historias', __name__, url_prefix='/historias')

@historia_bp.route('/', methods=['GET'])
def listar():
    try:
        return jsonify(controller.listar()), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@historia_bp.route('/<int:id>', methods=['GET'])
def buscar(id):
    try:
        historia = controller.buscar_por_id(id)
        if historia:
            return jsonify(historia), 200
        return jsonify({"mensagem": "História não encontrada"}), 404
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@historia_bp.route('/', methods=['POST'])
def criar():
    try:
        data = request.get_json()
        nova = controller.criar(data)
        return jsonify(nova), 201
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@historia_bp.route('/<int:id>', methods=['PUT'])
def atualizar(id):
    try:
        data = request.get_json()
        resultado = controller.atualizar(id, data)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@historia_bp.route('/<int:id>', methods=['DELETE'])
def excluir(id):
    try:
        resultado = controller.deletar(id)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
