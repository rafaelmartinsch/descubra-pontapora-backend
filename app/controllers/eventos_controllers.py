import app.models.eventos_model as model
from flask import request

def ordenados_por_data():
    try:
        eventos = model.ordenados_por_data()
        return eventos
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar eventos: {str(e)}")

def criar_evento(data):
    try:
        required_fields = ['titulo', 'descricao', 'local', 'data']
        missing = [field for field in required_fields if field not in data]
        if missing:
            raise ValueError(f"Campos obrigatórios faltando: {', '.join(missing)}")

        novo_evento = model.criar_evento(data)
        return novo_evento
    except Exception as e:
        raise RuntimeError(str(e))

def atualizar_evento(evento_id, data):
    try:
        if not data:
            raise ValueError('Nenhum dado fornecido para atualização')

        if not model.evento_existe(evento_id):
            return None

        evento_atualizado = model.atualizar_evento(evento_id, data)
        return evento_atualizado
    except Exception as e:
        raise RuntimeError(str(e))

def deletar_evento(evento_id):
    try:
        if not model.evento_existe(evento_id):
            return False

        return model.deletar_evento(evento_id)
    except Exception as e:
        raise RuntimeError(str(e))