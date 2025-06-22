import app.models.usuario_model as model

def listar_todos():
    return model.listar()
 
def buscar(id):
    return model.buscar(id)

def criar(dados):
    return model.criar(dados)

def atualizar(id, dados):
    return model.atualizar(id, dados)

def deletar(id):
    return model.deletar(id)