from app.services.db import conectar

def listar_eventos_ordenados_por_data():
    """
    Lista todos os eventos ordenados pela data em ordem ascendente.
    """
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """
            SELECT
            id,
            titulo,
            descricao,
            local,
            data,
            dt_fim,
            aberto,
            site,
            dt_cadastro
            FROM
            Eventos
            ORDER BY
            data ASC;
            """
    cursor.execute(sql)
    eventos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return eventos