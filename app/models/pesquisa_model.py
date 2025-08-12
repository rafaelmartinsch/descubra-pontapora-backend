from app.services.db import conectar
import logging

logger = logging.getLogger(__name__)

def search_all(query):
    try:
        if not query or len(query) > 100:
            return {"eventos": [], "historias": [], "locais": []}
            
        pattern = f"%{query}%"
        results = {"eventos": [], "historias": [], "locais": []}
        
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        
        # Search eventos
        cursor.execute("""
            SELECT id, titulo, descricao, 'evento' AS tipo
            FROM eventos
            WHERE 
                titulo LIKE %s OR 
                descricao LIKE %s OR 
                local LIKE %s
            ORDER BY 
                (titulo LIKE %s) DESC,
                LENGTH(titulo) ASC
            LIMIT 5
        """, (pattern, pattern, pattern, pattern))
        results["eventos"] = cursor.fetchall()
        
        # Search historias
        cursor.execute("""
            SELECT id, titulo, texto AS descricao, 'historia' AS tipo
            FROM historias
            WHERE 
                titulo LIKE %s OR 
                texto LIKE %s
            ORDER BY 
                (titulo LIKE %s) DESC,
                LENGTH(titulo) ASC
            LIMIT 5
        """, (pattern, pattern, pattern))
        results["historias"] = cursor.fetchall()
        
        # Search locais
        cursor.execute("""
            SELECT id, titulo, descricao, 'local' AS tipo
            FROM locais
            WHERE 
                titulo LIKE %s OR 
                descricao LIKE %s OR 
                detalhes LIKE %s OR 
                endereco LIKE %s
            ORDER BY 
                (titulo LIKE %s) DESC,
                LENGTH(titulo) ASC
            LIMIT 5
        """, (pattern, pattern, pattern, pattern, pattern))
        results["locais"] = cursor.fetchall()
        
        return results
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()