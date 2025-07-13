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
    imagens AS I ON I.origem_id = E.id AND I.capa = 1 AND I.capa='E'
ORDER BY
    E.data ASC;
            """
    cursor.execute(sql)
    eventos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return eventos