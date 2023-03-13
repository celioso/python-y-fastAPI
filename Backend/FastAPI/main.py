from fastapi import FastAPI 
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers

app.include_router(products.router)
app.include_router(users.router)

app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)


app.mount("/static", StaticFiles(directory= "static"), name="static")

# Url local: http://127.0.0.1:8000

@app.get("/")
async def root():
    return "¡Hola, Mundoo!"
# Url local: http://127.0.0.1:8000/url

@app.get("/url")
async def url():
    return {"url_curso": "https://fastapi.tiangolo.com/es/tutorial/first-steps/"}

# Inicia el server: uvicorn main:app --reload
# Detener el server: CTRL+C


"""if __name__ == '__main__':
    uvicorn.run(src='main.py:app', host="127.0.0.1", port=8000)"""

# Documentación con Swagger: http://127.0.0.1:8000/docs
# Documentación con Redocly: http://127.0.0.1:8000/redoc