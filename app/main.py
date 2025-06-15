from app.models import SorteioRequest
from fastapi import FastAPI

from app.core import realizar_sorteio

app = FastAPI()

@app.get("/")
def root():
    return {"Hello, World!"}

@app.post("/sortear")
def sortear(request: SorteioRequest):
    resultado = realizar_sorteio(request)
    return {"resultado": resultado}