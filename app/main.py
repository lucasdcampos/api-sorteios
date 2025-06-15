import os
from app.models import SorteioRequest
from fastapi import FastAPI, Header, HTTPException

from app.core import realizar_sorteio

app = FastAPI()

@app.get("/")
def root():
    return {"Hello, World!"}

@app.post("/sortear")
def sortear(request: SorteioRequest, x_api_key: str = Header(None)):
    api_key_env = os.getenv("API_KEY")
    print(api_key_env)
    if x_api_key != api_key_env:
        raise HTTPException(status_code=401, detail="API key inválida.")
    resultado = realizar_sorteio(request)
    return {"resultado": resultado}