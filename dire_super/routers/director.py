from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/directores",
                   tags=["director"])

class Director(BaseModel):
    id: int
    dni:str
    name:str
    surname:str
    email:str
    
    

director_list = [
    Director(id=1, dni="12345678A", name="Norman", surname="Perez", email="normanito.perez@example.com"),
    Director(id=2, dni="87654321B", name="Paquito", surname="Lope", email="daniel.lopez@example.com"),
    Director(id=3, dni="11223344C", name="Luis", surname="Garcia", email="luis.garcia@example.com"),
]


# Get all directores
@router.get("/")
def get_directors():
    return director_list

# Id
@router.get("/{id_directors}")
def get_director_by_id(id_directors: int):
    director = next((d for d in director_list if d.id == id_directors), None)
    if director:
        return director
    return {"error": "No directors with that ID not found"}

# DNI
@router.get("/dni/{dni}")
def get_director_by_dni(dni: str):
    journalist = next((d for d in director_list if d.dni.lower() == dni.lower()), None)
    if journalist:
        return journalist
    return {"error": "No directors with that DNI not found"}

# Name
@router.get("/name/{name}")
def get_director_by_name(name: str):
    results = [d for d in director_list if d.name.lower() == name.lower()]
    return results if results else {"error": "No directors found with that name"}

# Surname
@router.get("/surname/{surname}")
def get_director_by_surname(surname: str):
    results = [d for d in director_list if d.surname.lower() == surname.lower()]
    return results if results else {"error": "No directors found with that surname"}

# Email
@router.get("/email/{email}")
def get_director_by_telephone(email: str):
    results = [d for d in director_list if d.email == email]
    return results if results else {"error": "No directors found with that email"}

#Post
@router.post("/", status_code=201, response_model=Director)
def add_user(director: Director):
     director.id = next_id()
     director_list.append(director)
     return director


#put
@router.put("/{id}", response_model=Director)
def mod_director(id: int, director: Director):
    for index, saved_director in enumerate(director_list):
        if saved_director.id == id:
            director.id = id
            director_list[index] = saved_director
            return saved_director
    raise HTTPException(status_code=404, detail="Director no encontrado")

#delete
@router.delete("/{id}")
def del_user(id: int):
    for director in director_list:
        if director.id == id:
            director_list.remove(director)
            return{}
    raise HTTPException(status_code=404, detail="Director no encontrado") 

  

#calcular la id siguiente
def next_id():
    return (max(director_list, key=id).id+1)