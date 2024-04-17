from fastapi import FastAPI,Body
from  req import bRIF

app = FastAPI()

def sumar ():
    return 1+1
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/block")
def read_root(rif: str = Body(),stat:int =Body()):
    bRIF(rif,stat )
    return {"Status": "Exitoso"}


@app.post("/addCliente")
def read_root(rif: str = Body(),stat:int =Body()):
    bRIF(rif,stat )
    return {"Status": "Exitoso"}


