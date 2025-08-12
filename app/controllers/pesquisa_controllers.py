import app.models.pesquisa_model as model

def pesquisa(query):
    try:
        # Validate query
        if not query or len(query.strip()) < 2:
            return {"eventos": [], "historias": [], "locais": []}
            
        return model.search_all(query)
    except Exception as e:
        return None