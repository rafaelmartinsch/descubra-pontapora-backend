from app.services.db import conectar

def listar():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("Select * from usuarios")
    usuarios=cursor.fetchall()
    cursor.close()
    conexao.close()
    return usuarios
    
def buscar(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("Select id, nome, email, dt_cadastro from usuarios where id=%s", (id,))
    usuarios=cursor.fetchall()
    cursor.close()
    conexao.close()
    return usuarios
    
def criar(dados):
    conexao = conectar()
    cursor = conexao.cursor()
    sql =  "INSERT INTO usuarios(nome, email, senha, tipo) VALUES(%s, %s, %s, %s)"
    cursor.execute(sql, (dados['nome'], dados['email'], dados['senha'], dados['tipo']))
    conexao.commit()
    novo_id = cursor.lastrowid ##pegar o id do novo registro
    cursor.close()
    conexao.close()
    return novo_id

def atualizar(dados):
    conexao = conectar()
    cursor = conexao.cursor()
    sql =  "UPDATE usuarios SET nome=%s, tipo=%s WHERE id=%s "
    cursor.execute(sql, (dados['nome'], dados['tipo'], dados['id']))
    print(dados)
    conexao.commit()
    cursor.close()
    conexao.close()
    return

def atualizar_senha(id, hash):
    conexao = conectar()
    cursor = conexao.cursor()
    sql =  "UPDATE usuarios SET senha=%s  WHERE id=%s"
    cursor.execute(sql, (hash, id))
    conexao.commit()
    cursor.close()
    conexao.close()
    return

def deletar(id):
    conexao = conectar()
    cursor = conexao.cursor()
    sql =  "DELETE FROM usuarios WHERE id=%s"
    cursor.execute(sql, (id,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return