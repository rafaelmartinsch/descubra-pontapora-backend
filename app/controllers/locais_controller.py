import app.models.locais_model as model
import app.models.imagem_model as model_imagem

def listar_top4(grupo, tipo):
    tipo = tipo or ""
    return model.listar_top4(grupo, tipo)

def buscar_por_id(id):
    return model.buscar_por_id(id)

def listar_pontos_turisticos(categoria, subcategoria):
    return model.listar_pontos_turisticos(categoria, subcategoria)

def listar_estabelecimentos(categoria, subcategoria):
    return model.listar_estabelecimentos(categoria, subcategoria)

def inserir_ponto_turistico(dados):
    id = model.inserir_ponto_turistico(dados)
    model_imagem.inserir_capa(dados["capa"], dados["titulo"], tipo_origem='L', origem_id=id)
    return id

def atualizar_ponto_turistico(id, dados):
    return model.atualizar_ponto_turistico(id, dados)

def deletar_ponto_turistico(id):
    return model.deletar_ponto_turistico(id)

def inserir_estabelecimento(dados):
    return model.inserir_estabelecimento(dados)

def atualizar_estabelecimento(id, dados):
    return model.atualizar_estabelecimento(id, dados)

def deletar_estabelecimento(id):
    return model.deletar_estabelecimento(id)
