from app.services.db import conectar
from datetime import datetime

def listar():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT H.*, I.caminho AS capa
        FROM historias H
        LEFT JOIN imagens I ON I.origem_id = H.id AND I.capa = 1 AND I.tipo_origem = 'H'
        ORDER BY H.dt_cadastro DESC
    """)
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultado

def buscar_por_id(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("""
        SELECT H.*, I.caminho AS capa
        FROM historias H
        LEFT JOIN imagens I ON I.origem_id = H.id AND I.capa = 1 AND I.tipo_origem = 'H'
        WHERE H.id = %s
    """, (id,))
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resultado

def criar(data):
    """
    Cadastro de uma nova história ao BD.
    Args:
        data (dict): Conjunto de dados para serem alterados.
    Returns:
        tuple: dados do título, conteúdo, autor e data de atualização serão criados.
            - 
            
    """
    conexao = conectar()
    cursor = conexao.cursor()
    sql = "INSERT INTO historias (titulo, texto, autor, dt_cadastro) VALUES (%s, %s, %s, %s)"
    valores = (
        data['titulo'],
        data['conteudo'],
        data['autor'],
        data.get('data', datetime.now().date())  # se não enviar, usa hoje
    )
    cursor.execute(sql, valores)
    conexao.commit()
    id_novo = cursor.lastrowid
    cursor.close()
    conexao.close()
    return id_novo

def atualizar(id, data):
    """
    Atualiza uma história já publicada, onde apenas admin e editores têm permissão.
    Args:
        id (int): ID da história em específico.
        data (dict): Conjunto de dados para serem alterados.
    Returns:
        tuple: dados do título, conteúdo, autor e data de atualização serão mudados.
            - str: Título da história.
            - str: Conteúdo da história.
            - str: Autor da mudança.
            - datetime: Data da atualização.
    """
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        UPDATE historias
        SET titulo = %s, texto = %s, autor = %s, dt_cadastro = %s
        WHERE id = %s
    """
    valores = (
        data['titulo'],
        data['conteudo'],
        data['autor'],
        data.get('dt_cadastro', datetime.now().date()),
        id
    )
    cursor.execute(sql, valores)
    conexao.commit()
    cursor.close()
    conexao.close()
    return {"mensagem": "Notícia atualizada com sucesso"}

def deletar(id):
    """
    Exclui uma história unitariamente por base de um id
    Args:
        id (int): Id da história em específico
    Returns:
        None: 'Notícia removida com sucesso'
    """
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM historias WHERE id = %s", (id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return {"mensagem": "Notícia removida com sucesso"}

def listar_autores():
    """
    Retorna uma lista de administradores e editores para registrar um editar uma história.
        - 'A': Admin
        - 'E': Editor
    Returns:
        list: lista de admins e editores. 
    """
    pass
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id, nome FROM usuarios WHERE tipo IN ('A', 'E') ORDER BY nome")
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultado