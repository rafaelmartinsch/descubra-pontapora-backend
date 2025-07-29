import app.models.locais_model as model
import app.models.imagem_model as model_imagem

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
    tipo = tipo or ""
    return model.listar_top4(grupo, tipo)

def buscar_por_id(id):
    """
    Retorna um local específico pelo id (int) especificado.
    Args:
        id (int): O id do local.
    Returns:
        As informações para o evento específico no tipo RowType. Pode ser serializado diretamente em json sem precisar de conversão manual.
    """
    return model.buscar_por_id(id)

def listar_pontos_turisticos(categoria, subcategoria):
    """
    Retorna todos os pontos turísticos, aqueles em que o valor de 'grupo' = 'T', no banco de dados.
    Args:
        categoria (str, None): A categoria do local. No banco de dados está representada como 'tipo'. Opcional.
        subcategoria (str, None): A subcategoria do local. No banco de dados está representada como 'categoria'. Opcional
    Returns:
        Retorna todos os pontos turísticos no tipo List[RowType]. Serializável diretamente para JSON, sem conversão manual.
    """
    return model.listar_pontos_turisticos(categoria, subcategoria)

def listar_estabelecimentos(categoria, subcategoria):
    """
    Retorna todos os estabelecimentos, aqueles em que o valor de 'grupo' = 'E', no banco de dados.
    Args:
        categoria (str, None): A categoria do local. No banco de dados está representada como 'tipo'. Opcional.
        subcategoria (str, None): A subcategoria do local. No banco de dados está representada como 'categoria'. Opcional
    Returns:
        Retorna todos os pontos turísticos no tipo List[RowType]. Serializável diretamente para JSON, sem conversão manual.
    """
    return model.listar_estabelecimentos(categoria, subcategoria)

def inserir_ponto_turistico(dados):
    """
        Insere um ponto turístico (`tipo` (banco de dados) = 'T') na tabela locais no banco de dados. 
    Args:
        dados (str):  Um JSON com todas as informações do ponto turístico a serem inseridas.
    Returns:
        Retorna o ID do novo ponto turístico inserido.
    """
    id = model.inserir_ponto_turistico(dados)
    model_imagem.inserir_capa(dados["capa"], dados["titulo"], tipo_origem='L', origem_id=id)
    return id

def atualizar_ponto_turistico(id, dados):
    """
    Atualiza informação sobre o local, no banco de dados.
        Parâmetros:
        id (int): ID do registro
        dados (dict): Mesma estrutura de inserir_ponto_turistico()
    Retorno:
        int: Número de linhas afetadas (0 ou 1)
    """
    return model.atualizar_ponto_turistico(id, dados)

def deletar_ponto_turistico(id):
    """
    Remove ponto turístico do banco de dados.
    Parâmetros:
        id (int): ID do registro
    Retorno:
        int: Número de linhas afetadas
    """
    return model.deletar_ponto_turistico(id)

def inserir_estabelecimento(dados):
    """
    Adiciona o novo estabelecimento no banco de dados.
    Parâmetros :
        dados (dict): Mesma estrutura de inserir_estabelecimento()
    """
    return model.inserir_estabelecimento(dados)

def atualizar_estabelecimento(id, dados):
    """
    Atualiza informação do estabelecimento no banco de dados.
        Parâmetros:
        id (int): ID do registro
        dados (dict): Mesma estrutura de atualizar_estabelecimento()
    Retorno:
        int: Número de linhas afetadas (0 ou 1)
    """
    return model.atualizar_estabelecimento(id, dados)

def deletar_estabelecimento(id):
    """
    Remove o estabelecimento do banco de dados.
    Parâmetros:
        id (int): ID do registro
    Retorno:
        int: Número de linhas afetadas
    """
    return model.deletar_estabelecimento(id)
