from flask import Blueprint, jsonify, request
import app.controllers.usuario_controller as controller

usuario_bp=Blueprint('usuarios', __name__, url_prefix='/usuarios')

@usuario_bp.route('/', methods=['GET'])
def listar_usuarios():
    try:
        usuarios =  controller.listar_todos()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
    
@usuario_bp.route('/<int:id>', methods=['GET'])
def buscar(id):
    try:
        usuarios =  controller.buscar(id)
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
    
    
@usuario_bp.route('/', methods=['POST'])
def criar():
    try:
        dados = request.json
        novo_id=controller.criar(dados)
        return jsonify({'id': novo_id, 'mensagem':'Usuário criado com sucesso'}), 200
    
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
    
@usuario_bp.route('/<int:id>', methods=['PUT'])
def atualizar(id):
    try:
        dados = request.json
        controller.atualizar(id,dados)
        return jsonify({'id': id, 'mensagem':'Usuário atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@usuario_bp.route('/<int:id>', methods=['DELETE'])
def deletar(id):
    try:
        controller.deletar(id)
        return jsonify({'id': id, 'mensagem':'Usuário excluído com sucesso'}), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500