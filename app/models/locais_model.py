from app.services.db import conectar

def listar_top4(tipo):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """SELECT  titulo, img.caminho as capa, descricao, AVG(nota) as nota  
            FROM locais
            LEFT JOIN avaliacoes ON locais.id=local_id
            LEFT JOIN imagens img ON img.tipo_origem='L' 
                                    AND img.origem_id=locais.id 
                                    AND img.capa=1
            WHERE locais.tipo=%s
            GROUP BY titulo, descricao
            ORDER BY  nota DESC, titulo DESC
            LIMIT 4"""
    cursor.execute(sql, (tipo,))
    locais=cursor.fetchall()
    cursor.close()
    conexao.close()
    return locais