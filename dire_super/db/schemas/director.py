def director_schema(director) -> dict:
    return {"id": str(director["_id"]),
            "dni": director["dni"],
            "name": director["name"],
            "surname": director["surname"],
            "email": director["email"]}

def director_schema(directores) -> list:
    return [director_schema(director) for director in directores]