from app.services.db import conectar


def inserir_capa(caminho, legenda, tipo_origem, origem_id):
    conexao = conectar()
    cursor = conexao.cursor()
    sql = """
        INSERT INTO imagens (caminho, legenda, tipo_origem, origem_id, capa)
        VALUES (%s, %s, %s, %s, '1')
    """
    cursor.execute(sql, (
        caminho, legenda, tipo_origem, origem_id
    ))
    conexao.commit()
    id_inserido = cursor.lastrowid
    cursor.close()
    conexao.close()
    return id_inserido