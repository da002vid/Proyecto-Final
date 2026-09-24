from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


# ---------- Login ----------

class Token(BaseModel):
    access_token: str
    token_type: str


# ---------- Servicios ----------

class ServicioBase(BaseModel):
    nombre: str
    precio: float


class ServicioCreate(ServicioBase):
    pass


class ServicioUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None


class ServicioResponse(ServicioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ---------- Solicitudes ----------

class SolicitudBase(BaseModel):
    id_servicio: int
    fecha: date
    cliente: str


class SolicitudCreate(SolicitudBase):
    pass


class SolicitudUpdate(BaseModel):
    id_servicio: Optional[int] = None
    fecha: Optional[date] = None
    cliente: Optional[str] = None


class SolicitudResponse(SolicitudBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
