import app.models.eventos_model as model
import app.models.imagem_model as img_model
from datetime import datetime

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

        # Validação adicional de dados
        if len(data.get('titulo', '')) < 3 or len(data.get('titulo', '')) > 100:
            raise ValueError("O título deve ter entre 3 e 100 caracteres")
            
        if len(data.get('local', '')) < 3 or len(data.get('local', '')) > 100:
            raise ValueError("O local deve ter entre 3 e 100 caracteres")
            
        if len(data.get('descricao', '')) < 10 or len(data.get('descricao', '')) > 255:
            raise ValueError("A descrição deve ter entre 10 e 255 caracteres")
            
        # Validar datas
        try:
            datetime.fromisoformat(data['data'].replace('Z', '+00:00'))
        except ValueError:
            raise ValueError("Formato de data inválido")
            
        if 'dt_fim' in data and data['dt_fim']:
            try:
                datetime.fromisoformat(data['dt_fim'].replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("Formato de data final inválido")
                
            # Verificar se data final é posterior à data inicial
            data_inicio = datetime.fromisoformat(data['data'].replace('Z', '+00:00'))
            data_fim = datetime.fromisoformat(data['dt_fim'].replace('Z', '+00:00'))
            
            if data_fim <= data_inicio:
                raise ValueError("A data final deve ser posterior à data inicial")

        id_evento = model.criar_evento(data)
        return {'id': id_evento, 'mensagem': 'Evento criado com sucesso'}
    except Exception as e:
        raise RuntimeError(str(e))

def atualizar_evento(evento_id, data):
    try:
        if not data:
            raise ValueError('Nenhum dado fornecido para atualização')

        if not model.evento_existe(evento_id):
            return None

        # Validações semelhantes à criação
        if 'titulo' in data and (len(data['titulo']) < 3 or len(data['titulo']) > 100):
            raise ValueError("O título deve ter entre 3 e 100 caracteres")
            
        if 'local' in data and (len(data['local']) < 3 or len(data['local']) > 100):
            raise ValueError("O local deve ter entre 3 e 100 caracteres")
            
        if 'descricao' in data and (len(data['descricao']) < 10 or len(data['descricao']) > 255):
            raise ValueError("A descrição deve ter entre 10 e 255 caracteres")
            
        # Validar datas se fornecidas
        if 'data' in data and data['data']:
            try:
                datetime.fromisoformat(data['data'].replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("Formato de data inválido")
                
        if 'dt_fim' in data and data['dt_fim']:
            try:
                datetime.fromisoformat(data['dt_fim'].replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("Formato de data final inválido")
                
            # Se ambas as datas foram fornecidas, verificar se data final é posterior
            data_inicio_str = data['data'] if 'data' in data else None
            if not data_inicio_str:
                # Se não forneceu data inicial, buscar do banco
                eventos = model.ordenados_por_data()
                evento = next((e for e in eventos if e['id'] == evento_id), None)
                if evento:
                    data_inicio_str = evento['data']
            
            if data_inicio_str:
                data_inicio = datetime.fromisoformat(data_inicio_str.replace('Z', '+00:00'))
                data_fim = datetime.fromisoformat(data['dt_fim'].replace('Z', '+00:00'))
                
                if data_fim <= data_inicio:
                    raise ValueError("A data final deve ser posterior à data inicial")

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