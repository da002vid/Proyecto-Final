from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, crud
from ..seguridad import crear_token

router = APIRouter(
    tags=["Login"]
)


@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends()):
    usuario = crud.autenticar_usuario(form.username, form.password)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    token = crear_token(usuario.usuario)
    return {"access_token": token, "token_type": "bearer"}
