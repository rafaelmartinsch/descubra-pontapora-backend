from app.services.db import conectar

def listar_top4(tipo):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """
        SELECT locais.id, titulo, locais.tipo, img.caminho AS capa, descricao, AVG(nota) AS nota  
        FROM locais
        LEFT JOIN avaliacoes ON locais.id = local_id
        LEFT JOIN imagens img ON img.tipo_origem = 'L' 
            AND img.origem_id = locais.id 
            AND img.capa = 1
        WHERE locais.tipo = %s
        GROUP BY locais.id, titulo, locais.tipo, descricao, img.caminho
        ORDER BY nota DESC, titulo DESC
        LIMIT 4
    """
    cursor.execute(sql, (tipo,))
    locais = cursor.fetchall()
    cursor.close()
    conexao.close()
    return locais


def buscar_por_id(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """
        SELECT titulo, descricao, tipo, AVG(nota) AS nota, img.caminho AS capa
        FROM locais
        LEFT JOIN avaliacoes ON locais.id = local_id
        LEFT JOIN imagens img ON img.tipo_origem = 'L' 
            AND img.origem_id = locais.id 
            AND img.capa = 1
        WHERE locais.id = %s
        GROUP BY titulo, descricao, tipo, img.caminho
    """
    cursor.execute(sql, (id,))
    local = cursor.fetchone()
    cursor.close()
    conexao.close()
    return local
