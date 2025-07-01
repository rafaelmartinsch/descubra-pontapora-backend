from app.services.db import conectar

def ordenados_por_data():
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