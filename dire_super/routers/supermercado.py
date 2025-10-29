from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/supermercados",
                   tags=["supermercado"])


class Supermercado(BaseModel):
    id: int
    fecha: str
    superficie: float
    direccion: str
    id_director: int

#lista supermercados
sm_list = [
    Supermercado(id=1, fecha="12/05/2019", superficie=250.0, direccion="Calle Ejemplo 1", id_director=1),
    Supermercado(id=2, fecha="25/07/2020", superficie=320.5, direccion="Avenida Central 45", id_director=2),
    Supermercado(id=3, fecha="03/11/2021", superficie=180.0, direccion="Calle del Mercado 12", id_director=3),
    Supermercado(id=4, fecha="14/02/2022", superficie=400.0, direccion="Boulevard Los Pinos 78", id_director=4),
    Supermercado(id=5, fecha="08/08/2023", superficie=275.3, direccion="Calle Real 9", id_director=2),
    Supermercado(id=6, fecha="19/01/2024", superficie=510.7, direccion="Avenida del Sol 33", id_director=5),
    Supermercado(id=7, fecha="30/03/2024", superficie=360.0, direccion="Camino Verde 22", id_director=1),
    Supermercado(id=8, fecha="11/06/2024", superficie=295.8, direccion="Calle Norte 5", id_director=3),
    Supermercado(id=9, fecha="09/09/2024", superficie=420.4, direccion="Paseo del Río 17", id_director=4),
    Supermercado(id=10, fecha="05/10/2024", superficie=600.0, direccion="Avenida Libertad 100", id_director=5),
]

#get
@router.get("/")
def get_supers():
    return sm_list

#post
@router.post("/", status_code=201, response_model=Supermercado)
def add_super(super: Supermercado):
     super.id = next_id()
     sm_list.append(super)
     return super


#put
@router.put("/{id}", response_model=Supermercado)
def mod_super(id: int, super: Supermercado):
    for index, saved_super in enumerate(sm_list):
        if saved_super.id == id:
            super.id = id
            sm_list[index] = super
            return super
    raise HTTPException(status_code=404, detail="Supermercado no encontrado")

#delete
@router.delete("/{id}")
def del_super(id: int):
    for super in sm_list:
        if super.id == id:
            sm_list.remove(super)
            return{}
    raise HTTPException(status_code=404, detail="Supermercado no encontrado") 

  

#calcular la id siguiente
def next_id():
    return (max(sm_list, key=id).id+1)