from flask import Blueprint, jsonify, request
import app.controllers.locais_controller as controller

locais_bp = Blueprint('locais', __name__, url_prefix='/locais')

@locais_bp.route('/top4/', methods=['GET'])
def listar_top4():
    tipo = request.args.get('tipo')
    try:
        locais = controller.listar_top4(tipo)
        return jsonify(locais), 200
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

@locais_bp.route('/<int:id>', methods=['GET'])
def buscar_local(id):
    try:
        local = controller.buscar_por_id(id)
        if local:
            return jsonify(local), 200
        return jsonify({"mensagem": "Local não encontrado"}), 404
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500
