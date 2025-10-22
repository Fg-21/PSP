from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Supermercado(BaseModel):
    id: int
    fecha: str
    superficie: float
    direccion: str
    id_director: int

#lista supermercados
sm_list = [
    Supermercado(id= 1, fecha = "12/05/2019", superficie = 250.0, direccion = "Calle ejemplo", id_director= 1),
]

@app.get("/supermercados")
def get_supers():
    return sm_list