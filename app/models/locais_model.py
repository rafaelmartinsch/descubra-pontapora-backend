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
    """
    pass
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
    
    sql = """
        SELECT locais.*, AVG(nota) AS nota, img.caminho AS capa
        FROM locais
        LEFT JOIN avaliacoes ON locais.id = local_id
        LEFT JOIN imagens img ON img.tipo_origem = 'L' 
            AND img.origem_id = locais.id 
        WHERE locais.grupo = 'T'
    """
    
    params = []
    
    if categoria:
        sql += " AND locais.tipo = %s"
        params.append(categoria)
    
    if subcategoria:
        sql += " AND locais.categoria = %s"
        params.append(subcategoria)
    
    sql += """
        GROUP BY locais.id
        ORDER BY nota DESC, titulo DESC
    """
    
    cursor.execute(sql, params)
    locais = cursor.fetchall()
    cursor.close()
    conexao.close()
    return locais

def listar_estabelecimentos(categoria=None, subcategoria=None):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    
    sql = """
        SELECT locais.*, AVG(nota) AS nota, img.caminho AS capa
        FROM locais
        LEFT JOIN avaliacoes ON locais.id = local_id
        LEFT JOIN imagens img ON img.tipo_origem = 'L' 
            AND img.origem_id = locais.id 
        WHERE locais.grupo = 'E' 
    """
    
    params = []
    
    if categoria:
        sql += " AND locais.tipo = %s"
        params.append(categoria)
    
    if subcategoria:
        sql += " AND locais.categoria = %s"
        params.append(subcategoria)
    
    sql += """
        GROUP BY locais.id
        ORDER BY nota DESC, titulo DESC
    """
    
    cursor.execute(sql, params)
    locais = cursor.fetchall()
    cursor.close()
    conexao.close()
    return locais

def inserir_ponto_turistico(dados):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        INSERT INTO locais (titulo, descricao, tipo, categoria, grupo)
        VALUES (%s, %s, %s, %s, 'T')
    """
    cursor.execute(sql, (
        dados.get('titulo'),
        dados.get('descricao'),
        dados.get('tipo'),
        dados.get('categoria')
    ))
    conexao.commit()
    id_inserido = cursor.lastrowid
    cursor.close()
    conexao.close()
    return id_inserido

def atualizar_ponto_turistico(id, dados):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        UPDATE locais 
        SET titulo = %s, descricao = %s, tipo = %s, categoria = %s
        WHERE id = %s AND grupo = 'T'
    """
    cursor.execute(sql, (
        dados.get('titulo'),
        dados.get('descricao'),
        dados.get('tipo'),
        dados.get('categoria'),
        id
    ))
    conexao.commit()
    linhas_afetadas = cursor.rowcount
    cursor.close()
    conexao.close()
    return linhas_afetadas

def deletar_ponto_turistico(id):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "DELETE FROM locais WHERE id = %s AND grupo = 'T'"
    cursor.execute(sql, (id,))
    conexao.commit()
    linhas_afetadas = cursor.rowcount
    cursor.close()
    conexao.close()
    return linhas_afetadas

def inserir_estabelecimento(dados):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        INSERT INTO locais (titulo, descricao, tipo, categoria, grupo)
        VALUES (%s, %s, %s, %s, 'E')
    """
    cursor.execute(sql, (
        dados.get('titulo'),
        dados.get('descricao'),
        dados.get('tipo'),
        dados.get('categoria')
    ))
    conexao.commit()
    id_inserido = cursor.lastrowid
    cursor.close()
    conexao.close()
    return id_inserido

def atualizar_estabelecimento(id, dados):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        UPDATE locais 
        SET titulo = %s, descricao = %s, tipo = %s, categoria = %s
        WHERE id = %s AND grupo = 'E'
    """
    cursor.execute(sql, (
        dados.get('titulo'),
        dados.get('descricao'),
        dados.get('tipo'),
        dados.get('categoria'),
        id
    ))
    conexao.commit()
    linhas_afetadas = cursor.rowcount
    cursor.close()
    conexao.close()
    return linhas_afetadas

def deletar_estabelecimento(id):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "DELETE FROM locais WHERE id = %s AND grupo = 'E'"
    cursor.execute(sql, (id,))
    conexao.commit()
    linhas_afetadas = cursor.rowcount
    cursor.close()
    conexao.close()
    return linhas_afetadas
