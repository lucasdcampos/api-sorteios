from app.db import SupabaseDB

db = SupabaseDB()

def realizar_sorteio(request):
    return db.get_condominios() # retornando todos condominios para teste
