# db.py
from dotenv import load_dotenv
from supabase import create_client, Client
import os
from typing import List, Optional
from app.models import VagaUnidadeAtribuida

load_dotenv()

class SupabaseDB:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem ser definidos no ambiente.")
        self.client: Client = create_client(url, key)

    def get_usuarios(self):
        return self.client.table("usuarios").select("*").execute().data
    
    def get_condominios(self):
        return self.client.table("condominios").select("*").execute().data
    
    def get_vagas(self, condominio_id: Optional[int] = None):
        """Busca vagas, opcionalmente filtrando por ID do condomínio."""
        query = self.client.table("vagas").select("*")
        if condominio_id:
            query = query.eq("id_condominio", condominio_id)
        return query.execute().data
    
    def get_torres(self, condominio_id: Optional[int] = None):
        """Busca torres, opcionalmente filtrando por ID do condomínio."""
        query = self.client.table("torres").select("*")
        if condominio_id:
            query = query.eq("id_condominio", condominio_id)
        return query.execute().data
    
    def get_unidades(self, condominio_id: Optional[int] = None):
        """Busca unidades, opcionalmente filtrando por ID do condomínio."""
        query = self.client.table("unidades").select("*")
        if condominio_id:
            query = query.eq("id_condominio", condominio_id)
        return query.execute().data

    def salvar_resultado_sorteio(self, condominio_id: int, resultados: List[VagaUnidadeAtribuida]):
        """
        Salva o resultado completo de um sorteio no banco de dados.
        1. Cria um registro na tabela 'sorteios'.
        2. Salva os pares de vaga-unidade na tabela 'resultado_sorteios'.
        """
        try:
            # 'returning="representation"' faz a query retornar o dado inserido (ID do Sorteio).
            novo_sorteio_obj = (
                self.client.table("sorteios")
                .insert({"id_condominio": condominio_id}, returning="representation")
                .execute()
                .data
            )
            
            if not novo_sorteio_obj:
                raise Exception("Falha ao criar o registro do sorteio.")

            sorteio_id = novo_sorteio_obj[0]['sort_id']

            resultados_para_inserir = [
                {
                    "id_sorteio": sorteio_id,
                    "id_vaga": res.vaga_id,
                    "id_unidade": res.unidade_id,
                }
                for res in resultados
            ]

            if not resultados_para_inserir:
                # Caso não haja resultados, retorna o sorteio criado (vazio)
                return novo_sorteio_obj

            resultados_finais = (
                self.client.table("resultado_sorteios")
                .insert(resultados_para_inserir)
                .execute()
                .data
            )
            
            return {
                "sorteio": novo_sorteio_obj[0],
                "resultados": resultados_finais
            }

        except Exception as e:
            print(f"Erro ao salvar o sorteio no banco de dados: {e}")
            return None
    
    # Usando .neq("sort_id", 0) porque o supabase não permite deletar tudo sem condição, imbecilidade extrema
    def delete_resultado_sorteios(self):
        """
        Deleta todos os registros da tabela 'resultado_sorteios'.
        """
        try:
            self.client.table("resultado_sorteios").delete().neq("result_id", 0).execute()
        except Exception as e:
            print(f"Erro ao deletar resultados dos sorteios: {e}")

    def delete_sorteios(self):
        """
        Deleta todos os registros da tabela 'sorteios'.
        """
        try:
            self.client.table("sorteios").delete().neq("sort_id", 0).execute()
        except Exception as e:
            print(f"Erro ao deletar sorteios: {e}")
