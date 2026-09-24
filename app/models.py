from dataclasses import dataclass
from datetime import date


@dataclass
class Servicio:
    id: int
    nombre: str
    precio: float


@dataclass
class Solicitud:
    id: int
    id_servicio: int
    fecha: date
    cliente: str


@dataclass
class Usuario:
    id: int
    usuario: str
