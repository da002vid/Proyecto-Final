import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

CLAVE = os.getenv("SECRET_KEY")
oauth2 = OAuth2PasswordBearer(tokenUrl="/login")


def crear_token(usuario):
    vence = datetime.now(timezone.utc) + timedelta(minutes=60)
    datos = {
        "sub": usuario,
        "exp": int(vence.timestamp())
    }
    return jwt.encode(datos, CLAVE, algorithm="HS256")


def verificar_token(token: str = Depends(oauth2)):
    try:
        datos = jwt.decode(token, CLAVE, algorithms=["HS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido o vencido")
    return datos["sub"]
