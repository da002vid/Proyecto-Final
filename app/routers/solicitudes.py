from fastapi import APIRouter, Depends, HTTPException
from .. import schemas, crud
from ..seguridad import verificar_token

router = APIRouter(
    prefix="/solicitudes",
    tags=["Solicitud de servicios"],
    dependencies=[Depends(verificar_token)]
)


@router.get("/", response_model=list[schemas.SolicitudResponse])
def listar_solicitudes():
    return crud.get_solicitudes()


@router.get("/{solicitud_id}", response_model=schemas.SolicitudResponse)
def obtener_solicitud(solicitud_id: int):
    solicitud = crud.get_solicitud(solicitud_id)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return solicitud


@router.post("/", response_model=schemas.SolicitudResponse, status_code=201)
def crear_solicitud(solicitud: schemas.SolicitudCreate):
    servicio = crud.get_servicio(solicitud.id_servicio)
    if not servicio:
        raise HTTPException(status_code=400, detail="El servicio indicado no existe")
    return crud.create_solicitud(solicitud)


@router.put("/{solicitud_id}", response_model=schemas.SolicitudResponse)
def actualizar_solicitud(solicitud_id: int, datos: schemas.SolicitudUpdate):
    if datos.id_servicio is not None:
        servicio = crud.get_servicio(datos.id_servicio)
        if not servicio:
            raise HTTPException(status_code=400, detail="El servicio indicado no existe")

    solicitud = crud.update_solicitud(solicitud_id, datos)
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return solicitud


@router.delete("/{solicitud_id}", status_code=204)
def borrar_solicitud(solicitud_id: int):
    eliminada = crud.delete_solicitud(solicitud_id)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
