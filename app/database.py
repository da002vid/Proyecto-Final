import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def conectar():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    # Verifica que la conexión funcione al arrancar la app
    conexion = conectar()
    conexion.close()
