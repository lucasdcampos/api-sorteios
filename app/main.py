import os
from app.models import SorteioRequest
from fastapi import FastAPI, Header, HTTPException, Body

from app.core import realizar_sorteio, apagar_sorteios

app = FastAPI()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY não está definida no ambiente.")

@app.get("/")
def root():
    return {"AppSorteios": "API funcionando!"}

@app.get("/testar-rota-publica/")
def rota_publica():
    return {"AppSorteios": "Você acessou uma rota pública sem autenticação!"}

@app.get("/testar-rota-privada/")
def rota_privada(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida.")
    return {"AppSorteios": "Você acessou uma rota privada com autenticação! Autenticação bem-sucedida."}

@app.post("/sortear")
def sortear(request: SorteioRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida.")
    resultado = realizar_sorteio(request)
    return {"result": resultado}

@app.post("/nuke/sorteios")
def nuke_sorteios(
    message: str = Body(..., embed=True),
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida.")
    if message != "Now I am become death, the destroyer of worlds.":
        raise HTTPException(status_code=403, detail="Você não disse a frase.")
    result = apagar_sorteios()
    return {"result": result}