from app.models import historia_model as model
from app.models import imagem_model as imagem_model

def listar():
    return model.listar()

def buscar_por_id(id):
    return model.buscar_por_id(id)

def criar(data):
    id = model.criar(data)
    imagem_model.inserir_capa(data["caminho"], data["titulo"], "H", id)
    return id

def atualizar(id, data):
    return model.atualizar(id, data)

def deletar(id):
    return model.deletar(id)

def listar_autores():
    return model.listar_autores()
