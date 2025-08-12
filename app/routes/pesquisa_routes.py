from flask import Blueprint, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import app.controllers.pesquisa_controllers as controller

pesquisa_bp = Blueprint('pesquisa', __name__, url_prefix='/pesquisa')

# Initialize rate limiter (100 reqs/minute)
limiter = Limiter(key_func=get_remote_address)
def init_limiter(app):
    limiter.init_app(app)
    limiter.limit("200 per minute")(pesquisa_bp)

@pesquisa_bp.route('/teste', methods=['GET'])
def pesquisa():
    try:
        query = request.args.get('q', '').strip()
        resultados = controller.pesquisa(query)
        
        if resultados is None:
            return jsonify({"erro": "Pesquisa falhou"}), 500
            
        # Count total results
        resultados_totais = (
            len(resultados['eventos']) + 
            len(resultados['historias']) + 
            len(resultados['locais'])
        )
        
        return jsonify({
            "resultados": resultados,
            "resultados_totais": resultados_totais
        }), 200
        
    except Exception:
        return jsonify({"erro": "Requisição inválida"}), 400