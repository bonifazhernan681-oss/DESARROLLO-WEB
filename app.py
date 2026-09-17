"""
app.py
Proyecto Integrador U4 - Avance 14/16
Implementación de un sistema de login funcional.

Este archivo continúa la aplicación Flask desarrollada en la Semana 13.
Se incorpora un sistema de autenticación de usuarios con Flask-Login y
Werkzeug: registro de usuarios, almacenamiento de contraseñas mediante
hash, inicio de sesión, sesión activa, protección de rutas privadas y
cierre de sesión. El módulo de Productos (Cursos) sigue trabajando
contra MySQL (plataforma_cursos) sin cambios en su lógica CRUD.
"""

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import get_connection

from forms.curso_form import CursoForm
from forms.estudiante_form import EstudianteForm
from forms.instructor_form import InstructorForm
from forms.pago_form import PagoForm
from forms.usuario_form import RegistroForm, LoginForm

from models import Usuario, obtener_usuario_por_id, obtener_usuario_por_nombre

app = Flask(__name__)

# Clave secreta necesaria para la protección CSRF de Flask-WTF y para
# firmar la cookie de sesión que usa Flask-Login.
# En un entorno real, este valor debería cargarse desde una variable de entorno.
app.config['SECRET_KEY'] = 'clave-secreta-proyecto-integrador-2026'


# ------------------- CONFIGURACIÓN DE FLASK-LOGIN -------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Debe iniciar sesión para acceder a esta página.'
login_manager.login_message_category = 'warning'


@login_manager.user_loader
def load_user(id_usuario):
    """Flask-Login invoca esta función en cada request para recuperar,
    a partir del id guardado en la sesión, el objeto Usuario autenticado."""
    return obtener_usuario_por_id(id_usuario)


# ------------------- RUTA PRINCIPAL -------------------

@app.route('/')
def inicio():
    """Página principal informativa del proyecto (index.html). Es pública,
    no requiere sesión iniciada."""
    return render_template('index.html')


# ------------------- MÓDULO DE AUTENTICACIÓN -------------------

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Registra un nuevo usuario en la tabla usuarios. La contraseña se
    almacena protegida mediante generate_password_hash(), nunca en
    texto plano."""
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))

    form = RegistroForm()

    if form.validate_on_submit():
        if obtener_usuario_por_nombre(form.usuario.data):
            flash('Ese nombre de usuario ya está registrado.', 'danger')
            return render_template('registro.html', form=form)

        password_hash = generate_password_hash(form.password.data)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO usuarios (usuario, password) VALUES (%s, %s)',
            (form.usuario.data, password_hash)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Usuario registrado correctamente. Ya puede iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Valida las credenciales ingresadas contra la tabla usuarios y,
    si son correctas, crea la sesión del usuario mediante login_user()."""
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))

    form = LoginForm()

    if form.validate_on_submit():
        fila = obtener_usuario_por_nombre(form.usuario.data)

        if fila and check_password_hash(fila['password'], form.password.data):
            usuario_autenticado = Usuario(fila['id'], fila['usuario'])
            login_user(usuario_autenticado)
            flash(f'Bienvenido, {fila["usuario"]}.', 'success')

            siguiente = request.args.get('next')
            return redirect(siguiente or url_for('inicio'))

        flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """Finaliza la sesión del usuario autenticado mediante logout_user()."""
    logout_user()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('login'))


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
@login_required
def productos():
    """Muestra el catálogo de cursos recuperado directamente desde MySQL,
    incluyendo el nombre del instructor mediante un JOIN con instructores.
    Ruta protegida: requiere sesión iniciada."""
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
@login_required
def nuevo_producto():
    """Formulario de registro de un curso, validado con Flask-WTF y
    almacenado mediante INSERT en MySQL. Ruta protegida."""
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
@login_required
def editar_producto(id_curso):
    """Recupera un curso por su identificador, permite editarlo con el mismo
    formulario y guarda los cambios mediante UPDATE ... WHERE id_curso = %s.
    Ruta protegida."""
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
@login_required
def eliminar_producto(id_curso):
    """Elimina únicamente el curso seleccionado mediante DELETE ... WHERE id_curso = %s.
    Ruta protegida."""
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
@login_required
def clientes():
    """Muestra los estudiantes registrados (datos de ejemplo). Ruta protegida."""
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
@login_required
def nuevo_cliente():
    """Formulario de registro/edición de un estudiante, validado con Flask-WTF.
    Ruta protegida."""
    form = EstudianteForm()

    if form.validate_on_submit():
        flash(f'Estudiante "{form.nombre.data}" registrado correctamente.', 'success')
        return redirect(url_for('clientes'))

    return render_template('formulario_cliente.html', form=form)


# ------------------- MÓDULO PROVEEDORES (Instructores) -------------------

@app.route('/proveedores')
@login_required
def proveedores():
    """Muestra los instructores de la plataforma (datos de ejemplo). Ruta protegida."""
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
@login_required
def nuevo_proveedor():
    """Formulario de registro/edición de un instructor, validado con Flask-WTF.
    Ruta protegida."""
    form = InstructorForm()

    if form.validate_on_submit():
        flash(f'Instructor "{form.nombre.data}" registrado correctamente.', 'success')
        return redirect(url_for('proveedores'))

    return render_template('formulario_proveedor.html', form=form)


# ------------------- MÓDULO FACTURACIÓN (Pagos) -------------------

@app.route('/facturacion')
@login_required
def facturacion():
    """Muestra los pagos/matrículas registrados (datos de ejemplo). Ruta protegida."""
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
@login_required
def nuevo_pago():
    """Formulario de registro/edición de un pago, validado con Flask-WTF.
    Ruta protegida."""
    form = PagoForm()

    if form.validate_on_submit():
        flash(f'Pago "{form.numero.data}" registrado correctamente.', 'success')
        return redirect(url_for('facturacion'))

    return render_template('formulario_facturacion.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
