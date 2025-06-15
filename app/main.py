from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from app.core import realizar_sorteio

app = FastAPI()

class VagaUnidadeAtribuida(BaseModel):
    vaga_id: int
    unidade_id: int

class SorteioRequest(BaseModel):
    condominio_id: int
    torre_id: int
    vagas_atribuidas: List[VagaUnidadeAtribuida]

@app.get("/")
def root():
    return {"Hello, World!"}

@app.post("/sortear")
def sortear(request: SorteioRequest):
    resultado = realizar_sorteio(request)
    return {"resultado": resultado}