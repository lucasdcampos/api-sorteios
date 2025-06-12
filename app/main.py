from fastapi import FastAPI
from app.core import realizar_sorteio

app = FastAPI()

@app.get("/")
def root():
    return {"Hello, World!"}

@app.post("/sortear")
def sortear():
    resultado = realizar_sorteio()
    return {"resultado": resultado}
