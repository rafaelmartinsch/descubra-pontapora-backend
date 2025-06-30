from flask import Flask
from flask_cors import CORS
from .config import Config
from .routes import iniciar_rotas


def start_app():
    app = Flask(__name__)
    
    CORS(app, origins=["http://127.0.0.1:5500"])
    
    app.config.from_object(Config)
    iniciar_rotas(app)
    
    return app