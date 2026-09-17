"""
models.py
Proyecto Integrador U4 - Semana 14
Modelo de Usuario para el sistema de autenticación con Flask-Login.
"""

from flask_login import UserMixin
from conexion.conexion import get_connection


class Usuario(UserMixin):
    """Representa un usuario autenticado del sistema.

    UserMixin aporta las propiedades/métodos que Flask-Login necesita
    (is_authenticated, is_active, is_anonymous, get_id).
    """

    def __init__(self, id_usuario, usuario):
        self.id = id_usuario
        self.usuario = usuario

    def get_id(self):
        return str(self.id)


def obtener_usuario_por_id(id_usuario):
    """Recupera un usuario por su id. Usado por load_user() en cada
    request para reconstruir el objeto Usuario desde la sesión."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, usuario FROM usuarios WHERE id = %s', (id_usuario,))
    fila = cursor.fetchone()
    cursor.close()
    conn.close()

    if fila is None:
        return None
    return Usuario(fila['id'], fila['usuario'])


def obtener_usuario_por_nombre(usuario):
    """Recupera la fila completa (incluida la contraseña con hash) de un
    usuario según su nombre de usuario. Usado al registrar (para evitar
    duplicados) y al validar el login."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT id, usuario, password FROM usuarios WHERE usuario = %s', (usuario,))
    fila = cursor.fetchone()
    cursor.close()
    conn.close()
    return fila
