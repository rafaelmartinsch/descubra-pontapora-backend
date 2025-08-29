from app.services.db import conectar

def inserir_capa(caminho, legenda, tipo_origem, origem_id):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        INSERT INTO imagens (caminho, legenda, tipo_origem, origem_id, capa)
        VALUES (%s, %s, %s, %s, '1')
    """
    cursor.execute(sql, (caminho, legenda, tipo_origem, origem_id))
    conexao.commit()
    id_inserido = cursor.lastrowid
    cursor.close()
    conexao.close()
    return id_inserido

def existe_imagem_capa(tipo_origem, origem_id):
    """
    Verifica se já existe uma imagem de capa para a origem especificada.
    """
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        SELECT 1 FROM imagens 
        WHERE tipo_origem = %s AND origem_id = %s AND capa = 1
    """
    cursor.execute(sql, (tipo_origem, origem_id))
    exists = cursor.fetchone() is not None
    cursor.close()
    conexao.close()
    return exists

def atualizar_imagem_capa(caminho, legenda, tipo_origem, origem_id):
    """
    Atualiza a imagem de capa existente.
    """
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        UPDATE imagens 
        SET caminho = %s, legenda = %s
        WHERE tipo_origem = %s AND origem_id = %s AND capa = 1
    """
    cursor.execute(sql, (caminho, legenda, tipo_origem, origem_id))
    conexao.commit()
    cursor.close()
    conexao.close()

def deletar_imagem_capa(tipo_origem, origem_id):
    """
    Deleta a imagem de capa associada à origem especificada.
    """
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        DELETE FROM imagens 
        WHERE tipo_origem = %s AND origem_id = %s AND capa = 1
    """
    cursor.execute(sql, (tipo_origem, origem_id))
    conexao.commit()
    cursor.close()
    conexao.close()