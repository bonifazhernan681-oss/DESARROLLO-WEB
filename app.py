"""
app.py
Proyecto Integrador U4 - Avance 13/16
Uso de bases de datos relacionales: configuración, modelos y consultas básicas.

Este archivo continúa la aplicación Flask desarrollada en la Semana 12.
El módulo de Productos (Cursos), que hasta la Semana 12 usaba SQLite,
ahora trabaja directamente contra una base de datos relacional MySQL
(plataforma_cursos), mediante conexion/conexion.py. Se implementan las
cuatro operaciones completas: listar (SELECT con JOIN a instructores),
agregar (INSERT), modificar (UPDATE) y eliminar (DELETE).

Los módulos de Estudiantes, Instructores y Pagos se conservan con datos
de ejemplo, tal como en la Semana 12, y quedan preparados para incorporar
persistencia progresivamente.
"""

from flask import Flask, render_template, redirect, url_for, flash, request

from conexion.conexion import get_connection

from forms.curso_form import CursoForm
from forms.estudiante_form import EstudianteForm
from forms.instructor_form import InstructorForm
from forms.pago_form import PagoForm

app = Flask(__name__)

# Clave secreta necesaria para la protección CSRF de Flask-WTF.
# En un entorno real, este valor debería cargarse desde una variable de entorno.
app.config['SECRET_KEY'] = 'clave-secreta-proyecto-integrador-2026'


# ------------------- RUTA PRINCIPAL -------------------

@app.route('/')
def inicio():
    """Página principal informativa del proyecto (index.html)."""
    return render_template('index.html')


# ------------------- MÓDULO PRODUCTOS (Cursos) - MYSQL -------------------

def obtener_choices_instructores():
    """Consulta los instructores en MySQL y arma la lista de choices
    (id_instructor, nombre) para el SelectField del formulario de cursos."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id_instructor, nombre FROM instructores ORDER BY nombre')
    instructores = cursor.fetchall()
    cursor.close()
    conn.close()
    return [(id_instructor, nombre) for (id_instructor, nombre) in instructores]


@app.route('/productos')
def productos():
    """Muestra el catálogo de cursos recuperado directamente desde MySQL,
    incluyendo el nombre del instructor mediante un JOIN con instructores."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('''
        SELECT c.id_curso, c.nombre, c.descripcion, c.categoria,
               c.precio, c.cupos, c.id_instructor, i.nombre AS instructor
        FROM cursos c
        JOIN instructores i ON c.id_instructor = i.id_instructor
        ORDER BY c.id_curso DESC
    ''')
    cursos = cursor.fetchall()
    cursor.close()
    conn.close()

    total_cursos = len(cursos)

    return render_template('productos.html', cursos=cursos, total_cursos=total_cursos)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    """Formulario de registro de un curso, validado con Flask-WTF y
    almacenado mediante INSERT en MySQL."""
    form = CursoForm()
    form.id_instructor.choices = obtener_choices_instructores()

    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO cursos (nombre, descripcion, categoria, precio, cupos, id_instructor)
               VALUES (%s, %s, %s, %s, %s, %s)''',
            (form.nombre.data, form.descripcion.data, form.categoria.data,
             form.precio.data, form.cupos.data, form.id_instructor.data)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash(f'Curso "{form.nombre.data}" registrado correctamente.', 'success')
        return redirect(url_for('productos'))

    return render_template('formulario_producto.html', form=form, modo='nuevo')


@app.route('/productos/editar/<int:id_curso>', methods=['GET', 'POST'])
def editar_producto(id_curso):
    """Recupera un curso por su identificador, permite editarlo con el mismo
    formulario y guarda los cambios mediante UPDATE ... WHERE id_curso = %s."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM cursos WHERE id_curso = %s', (id_curso,))
    curso = cursor.fetchone()
    cursor.close()

    if curso is None:
        conn.close()
        flash('El curso solicitado no existe.', 'danger')
        return redirect(url_for('productos'))

    # En GET se precargan los datos actuales del curso en el formulario.
    form = CursoForm(data=curso) if request.method == 'GET' else CursoForm()
    form.id_instructor.choices = obtener_choices_instructores()

    if form.validate_on_submit():
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE cursos
               SET nombre = %s, descripcion = %s, categoria = %s,
                   precio = %s, cupos = %s, id_instructor = %s
               WHERE id_curso = %s''',
            (form.nombre.data, form.descripcion.data, form.categoria.data,
             form.precio.data, form.cupos.data, form.id_instructor.data, id_curso)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash(f'Curso "{form.nombre.data}" actualizado correctamente.', 'success')
        return redirect(url_for('productos'))

    conn.close()
    return render_template('formulario_producto.html', form=form, modo='editar', id_curso=id_curso)


@app.route('/productos/eliminar/<int:id_curso>', methods=['POST'])
def eliminar_producto(id_curso):
    """Elimina únicamente el curso seleccionado mediante DELETE ... WHERE id_curso = %s."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cursos WHERE id_curso = %s', (id_curso,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Curso eliminado correctamente.', 'success')
    return redirect(url_for('productos'))


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
