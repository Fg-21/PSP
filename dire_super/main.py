from fastapi import FastAPI
from routers import director, supermercado, auth_user, directorDb
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(director.router)
app.include_router(directorDb.router)
app.include_router(supermercado.router)
app.include_router(auth_user.router_user)
app.mount("/static", StaticFiles(directory="static"), name = "static")
    
@app.get("/")
def getGreeting():
    return {"detail": "Hello this is my API"}