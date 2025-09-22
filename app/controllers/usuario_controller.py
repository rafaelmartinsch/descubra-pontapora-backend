import hashlib
import app.models.usuario_model as model

def listar_todos():
    return model.listar()
 
def buscar(id):
    return model.buscar(id)

def criar(dados):
    senhaTxt = dados['senha']
    dados['senha'] = hashlib.sha256(senhaTxt.encode()).hexdigest() 
    return model.criar(dados)

def atualizar(dados):
    
    if dados['senha']:
        hash = hashlib.sha256(dados['senha'].encode()).hexdigest() 
        model.atualizar_senha(dados['id'], hash)
    return model.atualizar(dados)

def deletar(id):
    return model.deletar(id)

def login(login, senha):
    hash = hashlib.sha256(senha.encode()).hexdigest() 
    TIPO_MAP = {
        "A": "admin",
        "E": "editor",
        "V": "viewer"
    }

    dados = model.login(login, hash) 
    if dados: dados["tipo"] = TIPO_MAP[dados["tipo"]]

    return dados

