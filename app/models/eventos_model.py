from app.services.db import conectar
import html
from datetime import datetime

def ordenados_por_data():
    """
    Retorna todos os eventos ordenados pela data em ordem crescente, incluindo a imagem de capa.
    """
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """
    SELECT
        E.id,
        E.titulo,
        E.descricao,
        E.local,
        E.data,
        E.dt_fim,
        E.aberto,
        E.site,
        E.dt_cadastro,
        I.caminho AS caminho_imagem_capa,
        I.legenda AS legenda_imagem_capa
    FROM
        eventos AS E
    LEFT JOIN
        imagens AS I ON I.origem_id = E.id AND I.capa = 1 AND I.tipo_origem='E'
    ORDER BY
        E.data ASC;
    """
    cursor.execute(sql)
    eventos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return eventos

def criar_evento(data):
    """
    Insere um novo evento no banco de dados com os dados fornecidos.
    """
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        # Validação e escape dos dados
        titulo = html.escape(data.get('titulo', ''))
        descricao = html.escape(data.get('descricao', ''))
        local = html.escape(data.get('local', ''))
        data_evento = data.get('data', '')
        dt_fim = data.get('dt_fim', None)
        caminho_imagem_capa = data.get('caminho_imagem_capa', None)
        legenda_imagem_capa = data.get('legenda_imagem_capa', None)

        # Validação básica de datas
        if data_evento:
            try:
                datetime.fromisoformat(data_evento.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("Formato de data inválido")

        if dt_fim:
            try:
                datetime.fromisoformat(dt_fim.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError("Formato de data final inválido")

        sql = """
        INSERT INTO eventos (titulo, descricao, local, data, dt_fim)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (titulo, descricao, local, data_evento, dt_fim))
        conexao.commit()
        evento_id = cursor.lastrowid

        # Inserir imagem de capa se fornecida
        if caminho_imagem_capa:
            from app.models.imagem_model import inserir_capa
            inserir_capa(caminho_imagem_capa, legenda_imagem_capa, 'E', evento_id)

        return evento_id

    except Exception as e:
        if conexao:
            conexao.rollback()
        raise RuntimeError(f"Erro ao criar evento: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def evento_existe(evento_id):
    """
    Verifica se um evento com o ID fornecido existe no banco de dados.
    """
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT 1 FROM eventos WHERE id = %s", (evento_id,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conexao.close()
    return exists

def atualizar_evento(evento_id, data):
    """
    Atualiza os dados de um evento existente no banco de dados.
    """
    conexao = None
    cursor = None
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        
        # Colunas permitidas na tabela eventos
        allowed_columns = {
            'titulo', 'descricao', 'local', 'data', 'dt_fim', 'aberto', 'site'
        }
        
        # Validar colunas e construir cláusula SET segura
        set_parts = []
        values = []
        
        for col, val in data.items():
            if col in allowed_columns:
                # Aplicar escape HTML para prevenir XSS
                if isinstance(val, str) and col not in ['data', 'dt_fim']:
                    val = html.escape(val)
                set_parts.append(f"`{col}` = %s")
                values.append(val)
        
        if not set_parts:
            raise ValueError("Nenhuma coluna válida para atualização")
        
        # Adicionar evento_id para a cláusula WHERE
        values.append(evento_id)
        
        # Construir query parametrizada segura
        sql = f"""
            UPDATE eventos 
            SET {', '.join(set_parts)}
            WHERE id = %s
        """
        
        cursor.execute(sql, tuple(values))
        affected_rows = cursor.rowcount
        conexao.commit()
        
        # Atualizar imagem de capa se fornecida
        if 'caminho_imagem_capa' in data or 'legenda_imagem_capa' in data:
            from app.models.imagem_model import atualizar_imagem_capa
            caminho_imagem_capa = data.get('caminho_imagem_capa')
            legenda_imagem_capa = data.get('legenda_imagem_capa')
            
            # Verificar se já existe uma imagem de capa
            from app.models.imagem_model import existe_imagem_capa
            if existe_imagem_capa('E', evento_id):
                atualizar_imagem_capa(caminho_imagem_capa, legenda_imagem_capa, 'E', evento_id)
            else:
                from app.models.imagem_model import inserir_capa
                inserir_capa(caminho_imagem_capa, legenda_imagem_capa, 'E', evento_id)
        
        return {'id': evento_id, **data}
        
    except Exception as e:
        if conexao:
            conexao.rollback()
        if isinstance(e, ValueError):
            raise
        raise RuntimeError(f"Erro ao atualizar evento: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()

def deletar_evento(evento_id):
    """
    Deleta um evento do banco de dados com base no ID fornecido.
    """
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        # Primeiro deletar a imagem de capa associada
        from app.models.imagem_model import deletar_imagem_capa
        deletar_imagem_capa('E', evento_id)
        
        # Depois deletar o evento
        sql = "DELETE FROM eventos WHERE id = %s"
        cursor.execute(sql, (evento_id,))
        conexao.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conexao:
            conexao.rollback()
        raise RuntimeError(f"Erro ao deletar evento: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()