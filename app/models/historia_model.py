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

def buscar_por_id(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """
        SELECT 
            H.id, H.titulo, H.texto, H.autor, H.dt_cadastro,
            I.caminho AS capa
        FROM historias AS H
        LEFT JOIN imagens AS I 
            ON I.origem_id = H.id AND I.capa = 1 AND I.tipo_origem = 'H'
        WHERE H.id = %s
    """
    cursor.execute(sql, (id,))
    historia = cursor.fetchone()
    cursor.close()
    conexao.close()
    return historia
