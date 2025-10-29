from fastapi import FastAPI
from routers import director, supermercado
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(director.router)
app.include_router(supermercado.router)
app.mount("/static", StaticFiles(directory="static"), name = "static")
    
