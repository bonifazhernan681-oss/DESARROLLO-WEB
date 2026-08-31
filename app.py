"""
app.py
Proyecto Integrador U3 - Avance 11/16
Validación de formularios con Flask-WTF y WTForms.

Este archivo continúa la aplicación Flask desarrollada en la Semana 10,
incorporando formularios web con validación del lado del servidor mediante
Flask-WTF y WTForms, protección CSRF, y rutas GET/POST para el registro de
información en cada módulo. En esta etapa no se usa base de datos: los
datos siguen siendo de ejemplo (listas y diccionarios de Python) y los
formularios únicamente demuestran el proceso de validación.
"""

from flask import Flask, render_template, redirect, url_for, flash

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


# ------------------- MÓDULO PRODUCTOS (Cursos) -------------------

@app.route('/productos')
def productos():
    """Muestra el catálogo de cursos disponibles (datos de ejemplo)."""
    cursos = [
        {
            'nombre': 'Introducción a HTML5',
            'descripcion': 'Fundamentos de estructura y semántica web.',
            'categoria': 'Frontend',
            'precio': '$25.00',
            'cupos': 12
        },
        {
            'nombre': 'CSS3 y diseño responsive',
            'descripcion': 'Estilos, Flexbox, Grid y adaptabilidad a dispositivos.',
            'categoria': 'Frontend',
            'precio': '$30.00',
            'cupos': 0
        },
        {
            'nombre': 'JavaScript desde cero',
            'descripcion': 'Lógica de programación aplicada al navegador.',
            'categoria': 'Frontend',
            'precio': '$35.00',
            'cupos': 8
        },
        {
            'nombre': 'Python con Flask',
            'descripcion': 'Desarrollo de aplicaciones web con Python.',
            'categoria': 'Backend',
            'precio': '$40.00',
            'cupos': 5
        },
        {
            'nombre': 'Bases de datos relacionales',
            'descripcion': 'Modelado ER, SQL y administración de datos.',
            'categoria': 'Base de Datos',
            'precio': '$35.00',
            'cupos': 0
        },
        {
            'nombre': 'Despliegue en la nube',
            'descripcion': 'Publicación y escalado de aplicaciones web.',
            'categoria': 'DevOps',
            'precio': '$45.00',
            'cupos': 10
        },
    ]

    # Variable simple enviada desde Flask hacia la plantilla
    total_cursos = len(cursos)

    return render_template('productos.html', cursos=cursos, total_cursos=total_cursos)


@app.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    """Formulario de registro/edición de un curso, validado con Flask-WTF."""
    form = CursoForm()

    if form.validate_on_submit():
        # Todas las validaciones fueron satisfactorias.
        # La persistencia con MySQL/PostgreSQL se incorporará en avances posteriores;
        # por ahora solo se confirma el registro mediante un mensaje flash.
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
