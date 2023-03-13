from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "c9da80f2610d3ebfb5a1e2e34122a261e7acaaccde60e23802807268f0ef6244"

router = APIRouter(prefix="/jwtauth", 
                    tags= ["jwtauth"],
                    responses= {status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes = ["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled:bool

class UserDB(User):
    password: str

users_db = {
    "celismario":{
        "username": "celismario",
        "full_name": "Mario Restrepo Torres",
        "email": "falso@hotmail.com",
        "disabled":False,
        "password": "$2a$12$iDea8ecdNZv/2StqI.VZ6.rca/Bb.ejGZxurbCnapSEIZ/uIT6J46"
    },
    "camilotorres":{
        "username": "camilotorres",
        "full_name": "Camilo Fernando Acosta",
        "email": "falso2@hotmail.com",
        "disabled":True,
        "password": "$2a$12$Ij8l5VN5N2dsyYh3ePkE8eC6OPKxxnV3s5.OSauWLN6gKxd5RB2Um"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Credenciales de autenticación inválidas",
            headers= {"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
             raise exception

    except JWTError:
         raise exception
    
    return search_user(username)
    
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail = "Usuario inactivo")

    return user
    
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):                
        user_db = users_db.get(form.username)
        if not user_db:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST, 
                detail = "El usuario no es correcto, caught red handed")

        user = search_user_db(form.username)

        if not crypt.verify(form.password, user.password):
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST, 
                    detail = "La contraseña no es correcta")

        access_token = {"sub":user.username, 
             "exp":datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_DURATION)}
        
        return {"access_token":jwt.encode(access_token,SECRET, algorithm=ALGORITHM), "token_type":"bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user