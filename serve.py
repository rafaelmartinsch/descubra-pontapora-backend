from waitress import serve 
from app import start_app

# Cria a instância do Flask
app = start_app()

if __name__ == '__main__':
    # Rodando localmente para desenvolvimento
    serve(app, host='0.0.0.0', port=5000)