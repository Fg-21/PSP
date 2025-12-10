from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel
from db.models.director import Director
from db.schemas.director import director_schema, directores_schema
from db.client import db_client
from routers.auth_user import authentication
from bson import ObjectId

router = APIRouter(prefix="/directorDb",
                   tags=["directorDb"])

#Get
@router.get("/", response_model=list[Director])
def get_directors():
    return director_schema(db_client.test.directores.find())

@router.get("/{id}", response_model=Director)
def get_director_by_id(id: str):
    return search_dire_id(id)

#Post
@router.post("/", status_code=201)
async def add_dire(dire: Director):
    dire_ditch = dire.model_dump()
    del dire_ditch["id"]
    id = db_client.test.directores.insert_one(dire_ditch).inserted_id
    dire_ditch["id"] = str(id)

    return Director(**dire_ditch)





def search_dire_id(id: str):
    try:
        dire = director_schema(db_client.test.directores.find_one({"_id" : ObjectId(id)}))
        return Director(**dire)
    except:
        return{"error": "user not found"}