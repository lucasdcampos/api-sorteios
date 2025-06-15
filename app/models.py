from pydantic import BaseModel
from typing import List

class VagaUnidadeAtribuida(BaseModel):
    vaga_id: int
    unidade_id: int

class SorteioRequest(BaseModel):
    condominio_id: int
    torre_id: int
    vagas_atribuidas: List[VagaUnidadeAtribuida]