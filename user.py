from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

#Entidad post
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

usersLista = [User(id = 0, name = "Paca", surname = "Perezoa", age = 19),
              User(id = 1, name="Ana", surname="Gomez", age=22),
              User(id = 2, name="Luis", surname="Martinez", age=30),
              User(id = 3, name="Marta", surname="Lopez", age=25),
              User(id = 4, name="Carlos", surname="Sanchez", age=28),
              User(id = 5, name="Lucia", surname="Fernandez", age=21),
              User(id = 2, name="Jorge", surname="Diaz", age=35),
              User(id = 7, name="Elena", surname="Vargas", age=27),
              User(id = 8, name="Pedro", surname="Torres", age=33),
              User(id = 9, name="Sofia", surname="Ramirez", age=24)]

@app.get("/users/")
def users(id: int):
        return search_user(id)
    

@app.post("/users", status_code=201, response_model=User)
def add_user(user: User):
     user.id = next_id()
     usersLista.append(user)
     return user

@app.put("/users/{id}", response_model=User)
def mod_user(id: int, user: User):
    for index, saved_user in enumerate(usersLista):
        print(saved_user.id == id)
        if saved_user.id == id:
            user.id = id
            usersLista[index] = user
            return user
    raise HTTPException(status_code = 404, detail="Usuario no encontrado")    

@app.delete("/users/{id}")
def del_user(id: int):
    for user in usersLista:
        if user.id == id:
            usersLista.remove(user)
            return{}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")    


#devolver el siguiente id
def next_id():
     return (max(usersLista, key=id).id+1)

#buscar el usuario
def search_user(id: int):
    listaFiltrada = [obj for obj in usersLista if obj.id == id]
    if len(listaFiltrada) == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    else:
        return listaFiltrada
    
