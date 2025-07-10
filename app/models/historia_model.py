from app.services.db import conectar

def listar():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """
    SELECT
        H.*,
        I.caminho AS capa -- Retorna o caminho da imagem, ou NULL se não houver
    FROM
        historias AS H
    LEFT JOIN
        imagens AS I ON I.origem_id = H.id AND I.capa = 1 AND I.tipo_origem = 'H'
    ORDER BY
        H.dt_cadastro desc;
            """
    cursor.execute(sql)
    eventos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return eventos