from app.services.db import conectar

def ordenados_por_data():
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
    I.caminho AS caminho_imagem_capa, -- Retorna o caminho da imagem, ou NULL se não houver
    I.legenda AS legenda_imagem_capa   -- Opcional: Retorna a legenda da imagem também
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

from app.services.db import conectar

import html

def criar_evento(data):
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        # Escape HTML to prevent XSS
        titulo = html.escape(data.get('titulo', ''))
        descricao = html.escape(data.get('descricao', ''))
        local = html.escape(data.get('local', ''))
        data_evento = data.get('data', '')

        sql = """
        INSERT INTO eventos (titulo, descricao, local, data)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (titulo, descricao, local, data_evento))
        conexao.commit()
        evento_id = cursor.lastrowid

        return {'id': evento_id, 'titulo': titulo, 'descricao': descricao, 'local': local, 'data': data_evento}

    except Exception as e:
        conexao.rollback()
        raise RuntimeError(f"Erro ao criar evento: {str(e)}")

    finally:
        cursor.close()
        conexao.close()


def evento_existe(evento_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT 1 FROM eventos WHERE id = %s", (evento_id,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conexao.close()
    return exists

def atualizar_evento(evento_id, data):
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        set_clause = ', '.join([f"{k}=%s" for k in data])
        values = list(data.values()) + [evento_id]
        sql = f"UPDATE eventos SET {set_clause} WHERE id = %s"
        cursor.execute(sql, tuple(values))
        conexao.commit()
        return {'id': evento_id, **data}
    except Exception as e:
        conexao.rollback()
        raise RuntimeError(f"Erro ao atualizar evento: {str(e)}")
    finally:
        cursor.close()
        conexao.close()

def deletar_evento(evento_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "DELETE FROM eventos WHERE id = %s"
        cursor.execute(sql, (evento_id,))
        conexao.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conexao.rollback()
        raise RuntimeError(f"Erro ao deletar evento: {str(e)}")
    finally:
        cursor.close()
        conexao.close()