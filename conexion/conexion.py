"""
conexion/conexion.py
Proyecto Integrador U4 - Semana 13
Centraliza la conexión a la base de datos relacional (MySQL).

Todas las rutas del proyecto deben importar get_connection() desde este
módulo en lugar de crear conexiones sueltas dentro de app.py.
"""

import mysql.connector
from mysql.connector import Error

# Datos de conexión al servidor MySQL local.
# IMPORTANTE: no subir contraseñas reales al repositorio público de GitHub.
# En un entorno real, estos valores deberían cargarse desde variables de entorno.
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Hernan2026',
    'database': 'plataforma_cursos'
}


def get_connection():
    """Crea y devuelve una nueva conexión a la base de datos MySQL.

    Cada ruta debe abrir su propia conexión con esta función, usarla
    y cerrarla (junto con su cursor) al finalizar la operación.
    """
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        return conexion
    except Error as error:
        print(f'Error al conectar con MySQL: {error}')
        raise
