from pydantic import BaseModel
from typing import Optional

class Director(BaseModel):
    id: Optional[str]
    dni:str
    name:str
    surname:str
    email:str