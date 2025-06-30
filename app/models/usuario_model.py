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
    cursor.execute("Select * from usuarios where id=%s", (id,))
    usuarios=cursor.fetchall()
    cursor.close()
    conexao.close()
    return usuarios
    
def criar(dados):
    conexao = conectar()
    cursor = conexao.cursor()
    sql =  "INSERT INTO usuarios(nome, email, senha) VALUES(%s, %s, %s)"
    cursor.execute(sql, (dados['nome'], dados['email'], dados['senha']))
    conexao.commit()
    novo_id = cursor.lastrowid ##pegar o id do novo registro
    cursor.close()
    conexao.close()
    return novo_id

def atualizar(id, dados):
    conexao = conectar()
    cursor = conexao.cursor()
    sql =  "UPDATE usuarios SET nome=%s email=%s senha=%s WHERE id=%s"
    cursor.execute(sql, (dados['nome'], dados['email'], dados['senha'], id))
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