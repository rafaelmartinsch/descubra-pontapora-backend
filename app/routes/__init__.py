from .usuario_rotes import usuario_bp
from .locais_rotes import locais_bp
from .eventos_rotes import eventos_bp
from .historia_rotes import historia_bp

def iniciar_rotas(app):
    app.register_blueprint(usuario_bp)
    app.register_blueprint(locais_bp)
    app.register_blueprint(eventos_bp)
    app.register_blueprint(historia_bp)