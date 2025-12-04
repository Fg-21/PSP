from datetime import datetime, timezone, timedelta
from fastapi import Depends, FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
import jwt
from jwt import PyJWTError
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

users_db = {
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
    },
    "prueba": {
        
        "name": "prueba",
        "fullname": "SI López García",
        "email": "manolo@example.com",
        "disabled": False,
        "psw": "$argon2id$v=19$m=65536,t=3,p=4$8suSfQrvQeqZ9WhgtbWhmw$iJCW3cR9qd6+CcJksjqAJ8S29GRsTKbv1nATGgbiA5o" #1234
    
    }

    
}

@router_user.post("/register", status_code=201)
def register(user: UserDB):
    if user.name not in users_db:
        hashed_psw = password_hash.hash(user.psw)
        user.psw = hashed_psw
        users_db[user.name] = user.model_dump()
        return user
    else:
        raise HTTPException(status_code = 409, detail="User already exists")
    
@router_user.get("/register")
def getAllUsers():
    return users_db


@router_user.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if user_db:
        #Si el usuario existe comprobamos la contraseña
        user = UserDB(**user_db)
        try:
            if password_hash.verify(form.password, user.psw):
                    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
                    access_token = {"sub" : user.name, "exp" : expire}

                    #Generar token
                    token = jwt.encode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
                    return {"access_token": token, "token_type" : "bearer"}
        except:
            raise HTTPException(status_code=400, detail="Error al verificar contraseña")
    raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

async def authentication(token: str = Depends(oauth2)):
    username = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM]).get("sub")

    try: 
        if username is None:
            raise HTTPException(status_code=401, detail="Credenciales de autenticación inválidas", headers={"WWW.Authenticate" : "Bearer"})
    except PyJWTError:
         raise HTTPException(status_code=401, detail="Credenciales de autenticación inválidas", headers={"WWW.Authenticate" : "Bearer"})
        
    user = User(**users_db[username])

    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    return user

