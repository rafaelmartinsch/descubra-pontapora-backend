from flask import Flask
from flask_cors import CORS
from .config import Config
from .routes import iniciar_rotas

def start_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    CORS(app, origins=app.config["CORS_ORIGIN"])
    iniciar_rotas(app)
    
    return app