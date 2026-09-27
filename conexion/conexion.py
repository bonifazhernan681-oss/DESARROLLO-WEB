"""
conexion/conexion.py
Proyecto Integrador U4 - Semana 15
Centraliza la conexión a la base de datos relacional (PostgreSQL).

Todas las rutas del proyecto deben importar get_connection() (y, cuando
necesiten resultados como diccionario, get_dict_cursor()) desde este
módulo en lugar de crear conexiones sueltas dentro de app.py.

En Render, la variable de entorno DATABASE_URL es provista automáticamente
al enlazar una base de datos PostgreSQL con el servicio web. En desarrollo
local (sin esa variable definida) se usan los valores de DB_CONFIG.
"""

import os

import psycopg2
import psycopg2.extras
from psycopg2 import Error

# Datos de conexión para desarrollo local con PostgreSQL.
# La contraseña real NUNCA se escribe aquí: se lee de la variable de
# entorno DB_PASSWORD para no subirla al repositorio de GitHub. Ver
# instrucciones para configurarla en el equipo local en el README.
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 5432)),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'dbname': os.environ.get('DB_NAME', 'plataforma_cursos')
}

# Render entrega la cadena de conexión completa en DATABASE_URL.
DATABASE_URL = os.environ.get('DATABASE_URL')


def get_connection():
    """Crea y devuelve una nueva conexión a la base de datos PostgreSQL.

    Cada ruta debe abrir su propia conexión con esta función, usarla
    y cerrarla (junto con su cursor) al finalizar la operación.
    """
    try:
        if DATABASE_URL:
            # Render (y otros proveedores) exigen SSL para conexiones externas.
            return psycopg2.connect(DATABASE_URL, sslmode='require')
        return psycopg2.connect(**DB_CONFIG)
    except Error as error:
        print(f'Error al conectar con PostgreSQL: {error}')
        raise


def get_dict_cursor(conn):
    """Devuelve un cursor que entrega cada fila como diccionario
    (equivalente a cursor(dictionary=True) de mysql-connector)."""
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
