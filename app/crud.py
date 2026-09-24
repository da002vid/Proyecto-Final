import hashlib
from typing import Optional
import psycopg2
from . import models, schemas
from .database import conectar


# ==================== Usuarios ====================

def autenticar_usuario(usuario: str, contrasena: str) -> Optional[models.Usuario]:
    clave_encriptada = hashlib.sha256(contrasena.encode()).hexdigest()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, usuario FROM usuarios WHERE usuario = %s AND contrasena = %s",
        (usuario, clave_encriptada),
    )
    fila = cursor.fetchone()
    conn.close()
    if fila is None:
        return None
    return models.Usuario(id=fila[0], usuario=fila[1])


# ==================== Servicios ====================

def _fila_a_servicio(fila) -> models.Servicio:
    return models.Servicio(id=fila[0], nombre=fila[1], precio=float(fila[2]))


def get_servicios() -> list[models.Servicio]:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio FROM servicios ORDER BY id")
    filas = cursor.fetchall()
    conn.close()
    return [_fila_a_servicio(fila) for fila in filas]


def get_servicio(servicio_id: int) -> Optional[models.Servicio]:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nombre, precio FROM servicios WHERE id = %s",
        (servicio_id,),
    )
    fila = cursor.fetchone()
    conn.close()
    if fila is None:
        return None
    return _fila_a_servicio(fila)


def create_servicio(servicio: schemas.ServicioCreate) -> models.Servicio:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO servicios (nombre, precio) VALUES (%s, %s) RETURNING id, nombre, precio",
        (servicio.nombre, servicio.precio),
    )
    fila = cursor.fetchone()
    conn.commit()
    conn.close()
    return _fila_a_servicio(fila)


def update_servicio(
    servicio_id: int, datos: schemas.ServicioUpdate
) -> Optional[models.Servicio]:
    servicio = get_servicio(servicio_id)
    if not servicio:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(servicio, campo, valor)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE servicios SET nombre = %s, precio = %s WHERE id = %s",
        (servicio.nombre, servicio.precio, servicio.id),
    )
    conn.commit()
    conn.close()
    return servicio


def delete_servicio(servicio_id: int) -> bool:
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM servicios WHERE id = %s", (servicio_id,))
        eliminado = cursor.rowcount > 0
        conn.commit()
    except psycopg2.errors.ForeignKeyViolation:
        conn.rollback()
        raise ValueError("No se puede eliminar: el servicio tiene solicitudes")
    finally:
        conn.close()
    return eliminado


# ==================== Solicitudes ====================

def _fila_a_solicitud(fila) -> models.Solicitud:
    return models.Solicitud(
        id=fila[0], id_servicio=fila[1], fecha=fila[2], cliente=fila[3]
    )


def get_solicitudes() -> list[models.Solicitud]:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, id_servicio, fecha, cliente FROM solicitud_servicios ORDER BY id"
    )
    filas = cursor.fetchall()
    conn.close()
    return [_fila_a_solicitud(fila) for fila in filas]


def get_solicitud(solicitud_id: int) -> Optional[models.Solicitud]:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, id_servicio, fecha, cliente FROM solicitud_servicios WHERE id = %s",
        (solicitud_id,),
    )
    fila = cursor.fetchone()
    conn.close()
    if fila is None:
        return None
    return _fila_a_solicitud(fila)


def create_solicitud(solicitud: schemas.SolicitudCreate) -> models.Solicitud:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO solicitud_servicios (id_servicio, fecha, cliente) "
        "VALUES (%s, %s, %s) RETURNING id, id_servicio, fecha, cliente",
        (solicitud.id_servicio, solicitud.fecha, solicitud.cliente),
    )
    fila = cursor.fetchone()
    conn.commit()
    conn.close()
    return _fila_a_solicitud(fila)


def update_solicitud(
    solicitud_id: int, datos: schemas.SolicitudUpdate
) -> Optional[models.Solicitud]:
    solicitud = get_solicitud(solicitud_id)
    if not solicitud:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(solicitud, campo, valor)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE solicitud_servicios SET id_servicio = %s, fecha = %s, cliente = %s WHERE id = %s",
        (solicitud.id_servicio, solicitud.fecha, solicitud.cliente, solicitud.id),
    )
    conn.commit()
    conn.close()
    return solicitud


def delete_solicitud(solicitud_id: int) -> bool:
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM solicitud_servicios WHERE id = %s", (solicitud_id,))
    eliminada = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return eliminada
