from fastapi import APIRouter, Depends, HTTPException
from .. import schemas, crud
from ..seguridad import verificar_token

router = APIRouter(
    prefix="/servicios",
    tags=["Servicios"],
    dependencies=[Depends(verificar_token)]
)


@router.get("/", response_model=list[schemas.ServicioResponse])
def listar_servicios():
    return crud.get_servicios()


@router.get("/{servicio_id}", response_model=schemas.ServicioResponse)
def obtener_servicio(servicio_id: int):
    servicio = crud.get_servicio(servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio


@router.post("/", response_model=schemas.ServicioResponse, status_code=201)
def crear_servicio(servicio: schemas.ServicioCreate):
    return crud.create_servicio(servicio)


@router.put("/{servicio_id}", response_model=schemas.ServicioResponse)
def actualizar_servicio(servicio_id: int, datos: schemas.ServicioUpdate):
    servicio = crud.update_servicio(servicio_id, datos)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio


@router.delete("/{servicio_id}", status_code=204)
def borrar_servicio(servicio_id: int):
    try:
        eliminado = crud.delete_servicio(servicio_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    if not eliminado:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
