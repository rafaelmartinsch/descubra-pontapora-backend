from app.services.db import conectar

def listar_top4(grupo, tipo):
    """
    Retorna os 4 principais locais ordenados por nota ou ordem alfabética.
    Args:
        grupo (str): Código do grupo, podendo ser:
            - 'T': Tipo T
            - 'E': Tipo E
        tipo (str, optional): Filtro adicional para o tipo. Pode ser None.
    Returns:
        list: Lista com até 4 itens de destaque.
    Example:
        listar_top4("T")
        listar_top4("E", "promo")
    """
    pass  # implementação
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """
        SELECT locais.id, titulo, locais.tipo, img.caminho AS capa, descricao, AVG(nota) AS nota  
        FROM locais
        LEFT JOIN avaliacoes ON locais.id = local_id
        LEFT JOIN imagens img ON img.tipo_origem = 'L' 
            AND img.origem_id = locais.id 
            AND img.capa = 1
        WHERE locais.grupo = %s  AND locais.tipo LIKE %s
        GROUP BY locais.id, titulo, locais.tipo, descricao, img.caminho
        ORDER BY nota DESC, titulo DESC
        LIMIT 4
    """
    cursor.execute(sql, (grupo, '%'+tipo+'%'))
    locais = cursor.fetchall()
    cursor.close()
    conexao.close()
    return locais


def buscar_por_id(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """
        SELECT locais.* , AVG(nota) AS nota, img.caminho AS capa
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

def listar_pontos_turisticos(categoria=None, subcategoria=None):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    
    # Base da query
    sql = """
        SELECT locais.*, AVG(nota) AS nota, img.caminho AS capa
        FROM locais
        LEFT JOIN avaliacoes ON locais.id = local_id
        LEFT JOIN imagens img ON img.tipo_origem = 'L' 
            AND img.origem_id = locais.id 
        WHERE locais.tipo != 'Comércio'
    """
    
    params = []
    
    # Adiciona filtro de categoria se fornecida
    if categoria:
        sql += " AND locais.tipo = %s"
        params.append(categoria)
    
    # Adiciona filtro de subcategoria se fornecida
    if subcategoria:
        sql += " AND locais.categoria = %s"
        params.append(subcategoria)
    
    # Finaliza a query
    sql += """
        GROUP BY locais.id
        ORDER BY nota DESC, titulo DESC
    """
    
    cursor.execute(sql, params)
    locais = cursor.fetchall()
    cursor.close()
    conexao.close()
    return locais

def listar_todos_os_locais(categoria=None, subcategoria=None):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    
    # Base da query
    sql = """
        SELECT locais.*, AVG(nota) AS nota, img.caminho AS capa
        FROM locais
        LEFT JOIN avaliacoes ON locais.id = local_id
        LEFT JOIN imagens img ON img.tipo_origem = 'L' 
            AND img.origem_id = locais.id 
    """
    
    params = []
    
    # Adiciona filtro de categoria se fornecida
    if categoria:
        sql += " WHERE locais.tipo = %s"
        params.append(categoria)
    
    # Adiciona filtro de subcategoria se fornecida
    if subcategoria:
        sql += " AND locais.categoria = %s"
        params.append(subcategoria)
    
    # Finaliza a query
    sql += """
        GROUP BY locais.id
        ORDER BY nota DESC, titulo DESC
    """
    
    cursor.execute(sql, params)
    locais = cursor.fetchall()
    cursor.close()
    conexao.close()
    return locais