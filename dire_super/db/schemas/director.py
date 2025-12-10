def director_schema(director) -> dict:
    return {"id": str(director["_id"]),
            "dni": str(director["dni"]),
            "name": str(director["name"]),
            "surname": str(director["surname"]),
            "email": str(director["email"])}

def directores_schema(directores) -> list:
    return [director_schema(director) for director in directores]