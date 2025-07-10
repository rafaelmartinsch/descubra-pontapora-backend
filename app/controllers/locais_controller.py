import app.models.locais_model as model

def listar_top4(tipo):
    return model.listar_top4(tipo)

def buscar_por_id(id):
    return model.buscar_por_id(id)

def listar_pontos_turisticos(categoria, subcategoria):
    return model.listar_pontos_turisticos(categoria, subcategoria)

def listar_todos_os_locais(categoria, subcategoria):
    return model.listar_todos_os_locais(categoria, subcategoria)