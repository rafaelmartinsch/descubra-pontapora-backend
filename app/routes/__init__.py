from .usuario_rotes import usuario_bp
from .locais_rotes import locais_bp

def iniciar_rotas(app):
    app.register_blueprint(usuario_bp)
    app.register_blueprint(locais_bp)