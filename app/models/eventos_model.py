from app.services.db import conectar

def ordenados_por_data():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    sql = """
SELECT
    E.id,
    E.titulo,
    E.descricao,
    E.local,
    E.data,
    E.dt_fim,
    E.aberto,
    E.site,
    E.dt_cadastro,
    I.caminho AS caminho_imagem_capa, -- Retorna o caminho da imagem, ou NULL se não houver
    I.legenda AS legenda_imagem_capa   -- Opcional: Retorna a legenda da imagem também
FROM
    eventos AS E
LEFT JOIN
    imagens AS I ON I.origem_id = E.id AND I.capa = 1 AND I.tipo_origem='E'
ORDER BY
    E.data ASC;
            """
    cursor.execute(sql)
    eventos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return eventos

from app.services.db import conectar

import html

def criar_evento(data):
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        # Escape HTML to prevent XSS
        titulo = html.escape(data.get('titulo', ''))
        descricao = html.escape(data.get('descricao', ''))
        local = html.escape(data.get('local', ''))
        data_evento = data.get('data', '')

        sql = """
        INSERT INTO eventos (titulo, descricao, local, data)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (titulo, descricao, local, data_evento))
        conexao.commit()
        evento_id = cursor.lastrowid

        return {'id': evento_id, 'titulo': titulo, 'descricao': descricao, 'local': local, 'data': data_evento}

    except Exception as e:
        conexao.rollback()
        raise RuntimeError(f"Erro ao criar evento: {str(e)}")

    finally:
        cursor.close()
        conexao.close()


def evento_existe(evento_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT 1 FROM eventos WHERE id = %s", (evento_id,))
    exists = cursor.fetchone() is not None
    cursor.close()
    conexao.close()
    return exists

def atualizar_evento(evento_id, data):
    print(f"[DEBUG] Iniciando atualização para evento ID: {evento_id}")
    print(f"[DEBUG] Dados recebidos: {data}")
    
    conexao = None
    cursor = None
    try:
        print("[DEBUG] Conectando ao banco de dados...")
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        
        # Atualizado: Colunas permitidas na tabela eventos (excluindo id e dt_cadastro)
        allowed_columns = {
            'titulo', 'descricao', 'local', 'data', 'dt_fim', 'aberto', 'site'
        }
        print(f"[DEBUG] Colunas permitidas: {allowed_columns}")
        
        # Validar colunas e construir cláusula SET segura
        set_parts = []
        values = []
        invalid_columns = []
        
        print("[DEBUG] Processando colunas recebidas:")
        for col, val in data.items():
            if col in allowed_columns:
                print(f"  [VALID] {col} = {val} (aceito)")
                # Usar backticks para colunas reservadas como 'data' e 'local'
                set_parts.append(f"`{col}` = %s")
                values.append(val)
            else:
                print(f"  [INVALID] {col} (coluna não permitida)")
                invalid_columns.append(col)
        
        if invalid_columns:
            print(f"[WARN] Colunas inválidas ignoradas: {invalid_columns}")
        
        if not set_parts:
            print("[ERROR] Nenhuma coluna válida para atualização")
            raise ValueError("Nenhuma coluna válida para atualização")
        
        # Adicionar evento_id para a cláusula WHERE
        values.append(evento_id)
        
        # Construir query parametrizada segura
        sql = f"""
            UPDATE eventos 
            SET {', '.join(set_parts)}
            WHERE id = %s
        """
        print("[DEBUG] Query SQL gerada:")
        print(f"  SQL: {sql}")
        print(f"  Valores: {values}")
        
        print("[DEBUG] Executando query no banco...")
        cursor.execute(sql, tuple(values))
        affected_rows = cursor.rowcount
        print(f"[DEBUG] Query executada. Linhas afetadas: {affected_rows}")
        
        print("[DEBUG] Efetivando transação (commit)...")
        conexao.commit()
        print(f"[DEBUG] Commit realizado com sucesso")
        
        print(f"[DEBUG] Retornando resultado para ID {evento_id}")
        return {'id': evento_id, **data}
        
    except Exception as e:
        print(f"[ERROR] Exceção ocorrida: {str(e)}")
        if conexao:
            print("[DEBUG] Realizando rollback da transação...")
            conexao.rollback()
            print("[DEBUG] Rollback concluído")
        
        if isinstance(e, ValueError):
            print("[ERROR] Erro de validação - propagando exceção")
            raise
        print("[ERROR] Erro de banco de dados - gerando RuntimeError")
        raise RuntimeError(f"Erro ao atualizar evento: {str(e)}")
    finally:
        if cursor:
            print("[DEBUG] Fechando cursor")
            cursor.close()
        if conexao:
            print("[DEBUG] Fechando conexão com banco de dados")
            conexao.close()
        print("[DEBUG] Recursos liberados")

def deletar_evento(evento_id):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "DELETE FROM eventos WHERE id = %s"
        cursor.execute(sql, (evento_id,))
        conexao.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conexao.rollback()
        raise RuntimeError(f"Erro ao deletar evento: {str(e)}")
    finally:
        cursor.close()
        conexao.close()