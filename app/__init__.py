from flask import Flask
from flask_cors import CORS
from .config import Config
from .routes import iniciar_rotas

def start_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    CORS(app, origins=[
        "http://45.182.18.133:*",
        "https://45.182.18.133:*",
        "http://descubrapontapora.com.br:*",
        "https://descubrapontapora.com.br:*",
        "http://127.0.0.1:*"
    ])
    iniciar_rotas(app)
    
    return app