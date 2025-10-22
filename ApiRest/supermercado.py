from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Supermercado(BaseModel):
    id: int
    fecha:str
    superficie: float
    direccion: str
    id_director: int

#lista supermercados
sm_list = [
    Supermercado(1, "12/05/2019", 250, "Calle ejemplo", 1),
    Supermercado(2, "20/08/2020", 300, "Avenida Central 123", 2),
    Supermercado(3, "15/03/2021", 180, "Calle Norte 45", 1),
    Supermercado(4, "10/11/2018", 500, "Boulevard Sur 99", 3),
    Supermercado(5, "05/07/2022", 220, "Ruta Provincial 8 km 15", 2)
]

@app.get("/supermercados")
def get_supers():
    return sm_list