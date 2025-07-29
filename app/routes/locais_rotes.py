from flask import Blueprint, jsonify, request
import app.controllers.locais_controller as controller

locais_bp = Blueprint('locais', __name__, url_prefix='/locais')

@locais_bp.route('/estabelecimentos', methods=['GET'])
def listar_estabelecimentos():
    """
    Retorna todos os estabelecimentos.
    Returns:
        Retorna JSON dos dados retornados pelo banco de dados, sem necessidade de serialização manual.
    Throws:
        Retorna no JSON as exceções que ocorrerem das funções chamadas no escopo try.
    """
    categoria = request.args.get('categoria')
    subcategoria = request.args.get('subcategoria')
    try:
        locais = controller.listar_estabelecimentos(categoria, subcategoria)
        return jsonify(locais), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
    
@locais_bp.route('/turisticos', methods=['GET'])
def listar_pontos_turisticos():
    """
    Retorna todos os pontos turísticos.
    Returns:
        Retorna JSON dos dados retornados pelo banco de dados, sem necessidade de serialização manual.
    Throws:
        Retorna no JSON as exceções que ocorrerem das funções chamadas no escopo try.
    """
    categoria = request.args.get('categoria')
    subcategoria = request.args.get('subcategoria')
    try:
        locais = controller.listar_pontos_turisticos(categoria, subcategoria)
        return jsonify(locais), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@locais_bp.route('/top4/', methods=['GET'])
def listar_top4():
    """
    Retorna os 4 principais locais ordenados por nota ou ordem alfabética.
    Returns:
        Retorna JSON dos dados retornados pelo banco de dados, sem necessidade de serialização manual.
    Throws:
        Retorna no JSON as exceções que ocorrerem das funções chamadas no escopo try.
    """
    grupo = request.args.get('grupo')
    tipo = request.args.get('tipo')
    try:
        locais = controller.listar_top4(grupo, tipo)
        return jsonify(locais), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
    
@locais_bp.route('/<int:id>', methods=['GET'])
def buscar_local(id):
    """
    Retorna um local específico pelo id (int) especificado.
    Returns:
        Retorna JSON dos dados retornados pelo banco de dados, sem necessidade de serialização manual.
    Throws:
        Retorna no JSON as exceções que ocorrerem das funções chamadas no escopo try.
    """
    try:
        local = controller.buscar_por_id(id)
        if local:
            return jsonify(local), 200
        return jsonify({"mensagem": "Local não encontrado"}), 404
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
    
@locais_bp.route('/turisticos', methods=['POST'])
def criar_ponto_turistico():
    """
    Insere um ponto turístico no banco de dados. 
    Returns:
        Retorna JSON dos dados retornados pelo banco de dados, sem necessidade de serialização manual.
    Throws:
        Retorna no JSON as exceções que ocorrerem das funções chamadas no escopo try.
    """

    dados = request.json
    try:
        novo_id = controller.inserir_ponto_turistico(dados)
        return jsonify({'id': novo_id}), 201
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@locais_bp.route('/turisticos/<int:id>', methods=['PUT'])
def editar_ponto_turistico(id):
    dados = request.json
    try:
        linhas = controller.atualizar_ponto_turistico(id, dados)
        return jsonify({'mensagem': 'Atualizado com sucesso'}), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@locais_bp.route('/turisticos/<int:id>', methods=['DELETE'])
def excluir_ponto_turistico(id):
    try:
        linhas = controller.deletar_ponto_turistico(id)
        if linhas:
            return jsonify({'mensagem': 'Excluído com sucesso'}), 200
        return jsonify({'mensagem': 'Ponto turístico não encontrado'}), 404
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@locais_bp.route('/estabelecimentos', methods=['POST'])
def criar_estabelecimento():
    dados = request.json
    try:
        novo_id = controller.inserir_estabelecimento(dados)
        return jsonify({'id': novo_id}), 201
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@locais_bp.route('/estabelecimentos/<int:id>', methods=['PUT'])
def editar_estabelecimento(id):
    dados = request.json
    try:
        linhas = controller.atualizar_estabelecimento(id, dados)
        if linhas:
            return jsonify({'mensagem': 'Atualizado com sucesso'}), 200
        return jsonify({'mensagem': 'Estabelecimento não encontrado'}), 404
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@locais_bp.route('/estabelecimentos/<int:id>', methods=['DELETE'])
def excluir_estabelecimento(id):
    try:
        linhas = controller.deletar_estabelecimento(id)
        if linhas:
            return jsonify({'mensagem': 'Excluído com sucesso'}), 200
        return jsonify({'mensagem': 'Estabelecimento não encontrado'}), 404
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
