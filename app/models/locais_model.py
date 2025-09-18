from app.services.db import conectar

def listar_top4(grupo, tipo):
    """
    Retorna os 4 principais locais ordenados por ordem alfabética.
    A busca é filtrada pelos parâmetros opcionais.
    Args:
        grupo (str, optional): Código do grupo ('T' para Turístico, 'E' para Estabelecimento).
        tipo (str, optional): Filtro adicional para o tipo do local (ex: 'Praia', 'Restaurante').
    Returns:
        list: Lista com até 4 itens de destaque.
    """
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    sql = """
        SELECT locais.id, titulo, locais.tipo, img.caminho AS capa, descricao
        FROM locais
        LEFT JOIN imagens img ON img.tipo_origem = 'L'
            AND img.origem_id = locais.id
            AND img.capa = 1
    """

    conditions = []
    params = []

    if grupo:
        conditions.append("locais.grupo = %s")
        params.append(grupo)

    if tipo:
        conditions.append("locais.tipo LIKE %s")
        params.append(f"%{tipo}%")

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += """
        GROUP BY locais.id, titulo, locais.tipo, descricao, img.caminho
        ORDER BY titulo DESC
        LIMIT 4
    """

    cursor.execute(sql, tuple(params))
    locais = cursor.fetchall()
    cursor.close()
    conexao.close()
    return locais


def buscar_por_id(id):
    """
    Retorna um local específico pelo id (int) especificado.
    Args:
        id (int): O id do local.
    Returns:
        As informações para o evento específico no tipo RowType.
    """
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """
        SELECT locais.*, img.caminho AS capa
        FROM locais
        LEFT JOIN imagens img ON img.tipo_origem = 'L' 
            AND img.origem_id = locais.id 
            AND img.capa = 1
        WHERE locais.id = %s
        GROUP BY locais.id
    """
    cursor.execute(sql, (id,))
    local = cursor.fetchone()
    cursor.close()
    conexao.close()
    return local

def listar_pontos_turisticos(categoria=None, subcategoria=None):
    """
    Retorna todos os pontos turísticos.
    Args:
        categoria (str, None): A categoria do local (tipo). Opcional.
        subcategoria (str, None): A subcategoria do local (categoria). Opcional
    Returns:
        Retorna todos os pontos turísticos.
    """
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    
    sql = """
        SELECT locais.*, img.caminho AS capa
        FROM locais
        LEFT JOIN imagens img ON img.tipo_origem = 'L' AND img.origem_id = locais.id AND img.capa = 1
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
        ORDER BY locais.titulo ASC
    """
    
    cursor.execute(sql, params)
    locais = cursor.fetchall()
    cursor.close()
    conexao.close()
    return locais

def listar_estabelecimentos(categoria=None, subcategoria=None):
    """
    Retorna todos os estabelecimentos.
    Args:
        categoria (str, None): A categoria do local (tipo). Opcional.
        subcategoria (str, None): A subcategoria do local (categoria). Opcional
    Returns:
        Retorna todos os estabelecimentos.
    """
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    
    sql = """
        SELECT locais.*, img.caminho AS capa
        FROM locais
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
        ORDER BY titulo DESC
    """
    
    cursor.execute(sql, params)
    locais = cursor.fetchall()
    cursor.close()
    conexao.close()
    return locais

def inserir_ponto_turistico(dados):
    """
    Insere um ponto turístico na tabela locais.
    Args:
        dados (dict): Dicionário com as informações do ponto turístico.
    Returns:
        O ID do novo ponto turístico inserido.
    """
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        INSERT INTO locais (
            titulo, descricao, detalhes, tipo, categoria, endereco, 
            localiza_long, localiza_lat, hra_funcionamento, grupo
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'T')
    """
    cursor.execute(sql, (
        dados.get('titulo'),
        dados.get('descricao'),
        dados.get('detalhes'),
        dados.get('tipo'),
        dados.get('categoria'),
        dados.get('endereco'),
        dados.get('localiza_long'),
        dados.get('localiza_lat'),
        dados.get('hra_funcionamento')
    ))
    conexao.commit()
    id_inserido = cursor.lastrowid
    cursor.close()
    conexao.close()
    return id_inserido

def atualizar_ponto_turistico(id, dados):
    """
    Atualiza informação sobre o local no banco de dados.
    Args:
        id (int): ID do registro.
        dados (dict): Dicionário com os dados a serem atualizados.
    Returns:
        int: Número de linhas afetadas.
    """
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        UPDATE locais 
        SET 
            titulo = %s, descricao = %s, detalhes = %s, tipo = %s, categoria = %s, 
            endereco = %s, localiza_long = %s, localiza_lat = %s, hra_funcionamento = %s
        WHERE id = %s AND grupo = 'T'
    """
    cursor.execute(sql, (
        dados.get('titulo'),
        dados.get('descricao'),
        dados.get('detalhes'),
        dados.get('tipo'),
        dados.get('categoria'),
        dados.get('endereco'),
        dados.get('localiza_long'),
        dados.get('localiza_lat'),
        dados.get('hra_funcionamento'),
        id
    ))
    conexao.commit()
    linhas_afetadas = cursor.rowcount
    cursor.close()
    conexao.close()
    return linhas_afetadas

def deletar_ponto_turistico(id):
    """
    Remove ponto turístico do banco de dados.
    Args:
        id (int): ID do registro.
    Returns:
        int: Número de linhas afetadas.
    """
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
    """
    Adiciona o novo estabelecimento no banco de dados.
    Args:
        dados (dict): Dicionário com os dados do estabelecimento.
    """
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
    """
    Atualiza informação do estabelecimento no banco de dados.
    Args:
        id (int): ID do registro.
        dados (dict): Dicionário com os dados a serem atualizados.
    Returns:
        int: Número de linhas afetadas.
    """
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
         UPDATE locais 
        SET 
            titulo = %s, 
            descricao = %s, 
            tipo = %s, 
            categoria = %s,
            endereco = %s,
            hra_funcionamento = %s,
            site = %s
        WHERE id = %s AND grupo = 'E'
    """
    cursor.execute(sql, (
        dados.get('titulo'),
        dados.get('descricao'),
        dados.get('tipo'),
        dados.get('categoria'),     
        dados.get('endereco'),
        dados.get('hra_funcionamento'),
        dados.get('site'),
        id
    ))
    conexao.commit()
    linhas_afetadas = cursor.rowcount
    cursor.close()
    conexao.close()
    return linhas_afetadas

def deletar_estabelecimento(id):
    """
    Remove o estabelecimento do banco de dados.
    Args:
        id (int): ID do registro.
    Returns:
        int: Número de linhas afetadas.
    """
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "DELETE FROM locais WHERE id = %s AND grupo = 'E'"
    cursor.execute(sql, (id,))
    conexao.commit()
    linhas_afetadas = cursor.rowcount
    cursor.close()
    conexao.close()
    return linhas_afetadas

