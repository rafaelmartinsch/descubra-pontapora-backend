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
    return {"id": id_novo}

def atualizar(id, data):
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
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM historias WHERE id = %s", (id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return {"mensagem": "Notícia removida com sucesso"}

def listar_autores():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id, nome FROM usuarios WHERE tipo IN ('A', 'E') ORDER BY nome")
    resultado = cursor.fetchall()
    cursor.close()
    conexao.close()
    return resultado