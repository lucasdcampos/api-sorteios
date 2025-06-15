from dotenv import load_dotenv
from supabase import create_client, Client
import os

load_dotenv()

class SupabaseDB:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        self.client: Client = create_client(url, key)

    def get_usuarios(self):
        return self.client.table("usuarios").select("*").execute().data
    
    def get_condominios(self):
        return self.client.table("condominios").select("*").execute().data
    
    def get_vagas(self):
        return self.client.table("vagas").select("*").execute().data
    
    def get_torres(self):
        return self.client.table("torres").select("*").execute().data
    
    def get_unidades(self):
        return self.client.table("unidades").select("*").execute().data
    
    # Passando ID
    def get_vagas(self, condominio_id: int):
        return (
            self.client
            .table("vagas")
            .select("*")
            .eq("id_condominio", condominio_id)
            .execute()
            .data
        )
    
    def get_torres(self, condominio_id: int):
            return (
                self.client
                .table("vagas")
                .select("*")
                .eq("id_condominio", condominio_id)
                .execute()
                .data
            )

    def get_unidades(self, condominio_id: int):
        return (
            self.client
            .table("unidades")
            .select("*")
            .eq("id_condominio", condominio_id)
            .execute()
            .data
        )
