from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router_user = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl = "login")

#Algoritmo de encriptacion
ALGORITHM = "HS256"
#Caducidad
ACCESS_TOKEN_EXPIRE_MINUTES = 5
#Clave para la semilla para generar token
SECRET_KEY = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"

#Objeto para el hash de la contraseña
password_hash = PasswordHash.recommended()


class User(BaseModel):
    name : str
    fullname : str
    email : str
    disabled : bool

class UserDB(User):
    psw : str

user_db = {
    "manolo": {
        "name": "manolo",
        "fullname": "Manuel López García",
        "email": "manolo@example.com",
        "disabled": False,
        "psw": "manolo123"
    },
    "laura": {
        "name": "laura",
        "fullname": "Laura Fernández Ruiz",
        "email": "laura@example.com",
        "disabled": False,
        "psw": "lauraSecure!"
    },
    "carlos": {
        "name": "carlos",
        "fullname": "Carlos Pérez Díaz",
        "email": "carlos@example.com",
        "disabled": True,
        "psw": "carlospass2024"
    },
    "ana": {
        "name": "ana",
        "fullname": "Ana Gómez Torres",
        "email": "ana@example.com",
        "disabled": False,
        "psw": "AnaG_2025"
    },
    "si": {
        "name": "si",
        "fullname": "SI López García",
        "email": "manolo@example.com",
        "disabled": False,
        "psw": "$argon2id$v=19$m=65536,t=3,p=4$bBiplf1LSmuhjXKwPVkLwQ$czpjD9dnJyFXIEegFdRS5bfsybShO/K/4jUHazh0YeA"
    }
    
}

@router_user.post("/register", status_code=201)
def register(user: UserDB):
    if user.name not in user_db:
        hashed_psw = password_hash.hash(user.psw)
        user.psw = hashed_psw
        user_db[user.name] = user
        return user
    else:
        raise HTTPException(status_code = 409, detail="User already exists")
    
@router_user.get("/register")
def getAllUsers():
    return user_db
