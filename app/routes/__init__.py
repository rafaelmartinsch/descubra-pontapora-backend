from .usuario_routes import usuario_bp
from .locais_rotes import locais_bp
from .eventos_rotes import eventos_bp
from .historia_routes import historia_bp
from .pesquisa_routes import pesquisa_bp, init_limiter

def iniciar_rotas(app):
    app.register_blueprint(usuario_bp)
    app.register_blueprint(locais_bp)
    app.register_blueprint(eventos_bp)
    app.register_blueprint(historia_bp)
    app.register_blueprint(pesquisa_bp)
    init_limiter(app)