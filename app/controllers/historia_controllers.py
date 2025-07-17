from app.models import historia_model as model

def listar():
    return model.listar()

def buscar_por_id(id):
    return model.buscar_por_id(id)

def criar(data):
    return model.criar(data)

def atualizar(id, data):
    return model.atualizar(id, data)

def deletar(id):
    return model.deletar(id)
