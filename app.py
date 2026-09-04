"""
app.py
Proyecto Integrador U3 - Avance 12/16
Persistencia de datos en un entorno local con SQLite.

Este archivo continúa la aplicación Flask desarrollada en la Semana 11,
incorporando persistencia local con SQLite para el módulo de Cursos
(Productos). El flujo implementado es: Formulario -> Validación (Flask-WTF)
-> INSERT -> SELECT -> Tabla HTML (Jinja2). Los módulos de Estudiantes,
Instructores y Pagos se conservan con datos de ejemplo y quedan preparados
para incorporar persistencia progresivamente.
"""

import os
import sqlite3

from flask import Flask, render_template, redirect, url_for, flash

from forms.curso_form import CursoForm
from forms.estudiante_form import EstudianteForm
from forms.instructor_form import InstructorForm
from forms.pago_form import PagoForm

app = Flask(__name__)

# Clave secreta necesaria para la protección CSRF de Flask-WTF.
# En un entorno real, este valor debería cargarse desde una variable de entorno.
app.config['SECRET_KEY'] = 'clave-secreta-proyecto-integrador-2026'

# ------------------- CONFIGURACIÓN DE LA BASE DE DATOS -------------------

# Ruta local de la base de datos SQLite dentro de la carpeta data/
DB_PATH = os.path.join('data', 'ferreteria.db')


def get_db_connection():
    """Crea y devuelve una conexión a la base de datos SQLite.

    row_factory = sqlite3.Row permite acceder a las columnas por nombre
    (por ejemplo curso['nombre'] o curso.nombre en las plantillas Jinja2).
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crea la carpeta data/ y la tabla 'cursos' si aún no existen.

    Se usa CREATE TABLE IF NOT EXISTS para que la aplicación pueda
    reiniciarse cuantas veces sea necesario sin generar errores ni
    perder los datos ya almacenados.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            cupos INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# Se inicializa la base de datos al arrancar la aplicación.
init_db()


# ------------------- RUTA PRINCIPAL -------------------

@app.route('/')
def inicio():
    """Página principal informativa del proyecto (index.html)."""
    return render_template('index.html')


# ------------------- MÓDULO PRODUCTOS (Cursos) - CON PERSISTENCIA -------------------

@app.route('/productos')
def productos():
    """Muestra el catálogo de cursos recuperado desde SQLite."""
    conn = get_db_connection()
    cursos = conn.execute(
        'SELECT id, nombre, descripcion, categoria, precio, cupos FROM cursos ORDER BY id DESC'
    ).fetchall()
    conn.close()

    total_cursos = len(cursos)

    return render_template('productos.html', cursos=cursos, total_cursos=total_cursos)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    """Formulario de registro de un curso, validado con Flask-WTF y
    almacenado de forma persistente en SQLite."""
    form = CursoForm()

    if form.validate_on_submit():
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO cursos (nombre, descripcion, categoria, precio, cupos) VALUES (?, ?, ?, ?, ?)',
            (form.nombre.data, form.descripcion.data, form.categoria.data,
             form.precio.data, form.cupos.data)
        )
        conn.commit()
        conn.close()

        flash(f'Curso "{form.nombre.data}" registrado correctamente.', 'success')
        return redirect(url_for('productos'))

    return render_template('formulario_producto.html', form=form)


# ------------------- MÓDULO CLIENTES (Estudiantes) -------------------

@app.route('/clientes')
def clientes():
    """Muestra los estudiantes registrados (datos de ejemplo)."""
    estudiantes = [
        {'nombre': 'María Fernanda Loor', 'correo': 'maria.loor@correo.com',
         'curso': 'Introducción a HTML5', 'estado': 'Activo'},
        {'nombre': 'Carlos Andrés Zambrano', 'correo': 'carlos.zambrano@correo.com',
         'curso': 'Python con Flask', 'estado': 'Activo'},
        {'nombre': 'Génesis Priscila Vera', 'correo': 'genesis.vera@correo.com',
         'curso': 'CSS3 y diseño responsive', 'estado': 'Inactivo'},
        {'nombre': 'Jonathan David Chávez', 'correo': 'jonathan.chavez@correo.com',
         'curso': 'Bases de datos relacionales', 'estado': 'Activo'},
    ]
    return render_template('clientes.html', estudiantes=estudiantes)


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():
    """Formulario de registro/edición de un estudiante, validado con Flask-WTF."""
    form = EstudianteForm()

    if form.validate_on_submit():
        flash(f'Estudiante "{form.nombre.data}" registrado correctamente.', 'success')
        return redirect(url_for('clientes'))

    return render_template('formulario_cliente.html', form=form)


# ------------------- MÓDULO PROVEEDORES (Instructores) -------------------

@app.route('/proveedores')
def proveedores():
    """Muestra los instructores de la plataforma (datos de ejemplo)."""
    instructores = [
        {'nombre': 'Ing. Paola Ramírez', 'especialidad': 'Frontend y UX/UI',
         'correo': 'paola.ramirez@desarrolloweb.com'},
        {'nombre': 'Ing. Diego Salazar', 'especialidad': 'Backend con Python',
         'correo': 'diego.salazar@desarrolloweb.com'},
        {'nombre': 'Ing. Lucía Torres', 'especialidad': 'Bases de Datos',
         'correo': 'lucia.torres@desarrolloweb.com'},
    ]
    return render_template('proveedores.html', instructores=instructores)


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def nuevo_proveedor():
    """Formulario de registro/edición de un instructor, validado con Flask-WTF."""
    form = InstructorForm()

    if form.validate_on_submit():
        flash(f'Instructor "{form.nombre.data}" registrado correctamente.', 'success')
        return redirect(url_for('proveedores'))

    return render_template('formulario_proveedor.html', form=form)


# ------------------- MÓDULO FACTURACIÓN (Pagos) -------------------

@app.route('/facturacion')
def facturacion():
    """Muestra los pagos/matrículas registrados (datos de ejemplo)."""
    pagos = [
        {'numero': 'F-001', 'estudiante': 'María Fernanda Loor',
         'curso': 'Introducción a HTML5', 'monto': '$25.00', 'fecha': '01/08/2026'},
        {'numero': 'F-002', 'estudiante': 'Carlos Andrés Zambrano',
         'curso': 'Python con Flask', 'monto': '$40.00', 'fecha': '05/08/2026'},
        {'numero': 'F-003', 'estudiante': 'Jonathan David Chávez',
         'curso': 'Bases de datos relacionales', 'monto': '$35.00', 'fecha': '10/08/2026'},
    ]
    return render_template('facturacion.html', pagos=pagos)


@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
def nuevo_pago():
    """Formulario de registro/edición de un pago, validado con Flask-WTF."""
    form = PagoForm()

    if form.validate_on_submit():
        flash(f'Pago "{form.numero.data}" registrado correctamente.', 'success')
        return redirect(url_for('facturacion'))

    return render_template('formulario_facturacion.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)