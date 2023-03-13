from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users", 
                    tags= ["users"],
                    responses= {404:{"message":"No encontrado"}})

# Url local: http://127.0.0.1:8000
# Inicio del servidor uvicorn users:app --reload

# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url:str
    age:int

users_list = [User(id=1, name = "Camilo",surname =  "Torres",url ="https://www.baloto.com/",age = 35), 
User(id=2,name =  "Alvero",surname ="Rojas",url ="https://www.megamillions.com/",age = 29), 
User(id=3,name = "German",surname = "Bejarano",url ="https://powerball.com/",age = 34)
]

@router.get("/usersjson")
async def usersjson():
    return [
        {"name":"Mario", "surname": "celis", "url":"https://www.baloto.com/","age": 38},
        {"name":"Alex", "surname": "loco", "url":"https://www.megamillions.com/", "age": 25},
        {"name":"Camilo", "surname": "pez", "url":"https://powerball.com/", "age": 30}
]


@router.get("/users")
async def users():
    return users_list

# Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

# Query 


@router.get("/user/")  # Visualiza en contenido
async def user(id: int, name: str):
    return search_user(id)

@router.post("/user/",response_model = User, status_code=201) # Agregar un usuario
async def user(user:User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="El usuario ya existe 👍👍👽👽")
        #return {"Error☠️☠️":"El usuario ya existe 👍👍👽👽"}
    else:
        users_list.append(user)
        return user
        #print("El usuario se agregó exitosamente👌👌🤖🤖") # Averiguar como colocar mensage de usuario agregado

@router.put("/user/")  # Actualizar un usuario
async def user(user:User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"Error":"No se ha actualizado el usuario"}
    
    return user

@router.delete("/user/{id}")
async def user(id:int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"Error":"No se ha eliminado el usuario"}



def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error":"No se ha encontrado el usuario"}

# http://127.0.0.1:8000/user/?id=1&Camilo ; para colocar dos parametros

