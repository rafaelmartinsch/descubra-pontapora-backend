from app.services.db import conectar

def listar_top4(grupo, tipo):
    """
    Retorna os 4 principais locais ordenados por nota ou ordem alfabética, utilizado na index do site
    Args:
        grupo (str): Código do grupo, podendo ser:
            - 'T': Tipo Turistico
            - 'E': Tipo Estabelecimentos
        tipo (str): Filtro adicional para o tipo. Pode ser None.
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
    """
    Retorna um local específico pelo id (int) especificado.
    Args:
        id (int): O id do local.
    Returns:
        As informações para o evento específico no tipo RowType. Pode ser serializado diretamente em json sem precisar de conversão manual.
    """
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
    """
    Retorna todos os pontos turísticos, aqueles em que o valor de 'grupo' = 'T', no banco de dados.
    Args:
        categoria (str, None): A categoria do local. No banco de dados está representada como 'tipo'. Opcional.
        subcategoria (str, None): A subcategoria do local. No banco de dados está representada como 'categoria'. Opcional
    Returns:
        Retorna todos os pontos turísticos no tipo List[RowType]. Serializável diretamente para JSON, sem conversão manual.
    """
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
    """
    Retorna todos os estabelecimentos, aqueles em que o valor de 'grupo' = 'E', no banco de dados.
    Args:
        categoria (str, None): A categoria do local. No banco de dados está representada como 'tipo'. Opcional.
        subcategoria (str, None): A subcategoria do local. No banco de dados está representada como 'categoria'. Opcional
    Returns:
        Retorna todos os pontos turísticos no tipo List[RowType]. Serializável diretamente para JSON, sem conversão manual.
    """
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
    """
        Insere um ponto turístico (`tipo` (banco de dados) = 'T') na tabela locais no banco de dados. 
    Args:
        dados (str):  Um JSON com todas as informações do ponto turístico a serem inseridas.
    Returns:
        Retorna o ID do novo ponto turístico inserido.
    """
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
    """
    Atualiza informação sobre o local, no banco de dados.
        Parâmetros:
        id (int): ID do registro
        dados (dict): Mesma estrutura de inserir_ponto_turistico()
    Retorno:
        int: Número de linhas afetadas (0 ou 1)
    """

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
    """
    Remove ponto turístico do banco de dados.
    Parâmetros:
        id (int): ID do registro
    Retorno:
        int: Número de linhas afetadas
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
    Parâmetros :
        dados (dict): Mesma estrutura de inserir_estabelecimento()
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
        Parâmetros:
        id (int): ID do registro
        dados (dict): Mesma estrutura de atualizar_estabelecimento()
    Retorno:
        int: Número de linhas afetadas (0 ou 1)
    """
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
    """
    Remove o estabelecimento do banco de dados.
    Parâmetros:
        id (int): ID do registro
    Retorno:
        int: Número de linhas afetadas
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
