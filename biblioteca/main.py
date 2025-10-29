from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import autores, libros

app=FastAPI()


app.include_router(autores.router)
app.include_router(libros.router)
app.mount("/static", StaticFiles(directory="static"), name = "static")  


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")


def root():
    return{"Hello":"World"}