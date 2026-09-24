from contextlib import asynccontextmanager
from fastapi import FastAPI

from .database import init_db
from .routers import login, servicios, solicitudes


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Proyecto Final", version="1.0.0", lifespan=lifespan)

app.include_router(login.router)
app.include_router(servicios.router)
app.include_router(solicitudes.router)


@app.get("/")
def inicio():
    return {"mensaje": "API del proyecto final funcionando"}
