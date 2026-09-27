"""
app.py
Proyecto Integrador U4 - Avance 15/16
Construcción de una aplicación con funciones CRUD sobre PostgreSQL.

Continúa la aplicación Flask de las semanas anteriores. Los cuatro
módulos principales (Cursos, Estudiantes, Instructores, Pagos) quedan
conectados a PostgreSQL con operaciones completas de Crear, Leer,
Actualizar y Eliminar, usando siempre consultas parametrizadas. El
sistema de login de la Semana 14 (Flask-Login + Werkzeug) se mantiene
funcionando sin cambios en su lógica, solo migrado a PostgreSQL.
"""

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import get_connection, get_dict_cursor

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


# ------------------- MÓDULO PRODUCTOS (Cursos) -------------------

def obtener_choices_instructores():
    """Consulta los instructores en PostgreSQL y arma la lista de choices
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
    """Muestra el catálogo de cursos recuperado directamente desde
    PostgreSQL, incluyendo el nombre del instructor mediante un JOIN
    con instructores. Ruta protegida: requiere sesión iniciada."""
    conn = get_connection()
    cursor = get_dict_cursor(conn)
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
    almacenado mediante INSERT en PostgreSQL. Ruta protegida."""
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
    cursor = get_dict_cursor(conn)
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
    Ruta protegida.

    Nota: si el curso tiene pagos asociados, PostgreSQL rechazará el
    DELETE por la FOREIGN KEY de pagos.id_curso (integridad referencial);
    en ese caso se informa el error al usuario en vez de dejar pagos
    "huérfanos" o mostrar una pantalla de error técnico."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM cursos WHERE id_curso = %s', (id_curso,))
        conn.commit()
        flash('Curso eliminado correctamente.', 'success')
    except Exception:
        conn.rollback()
        flash('No se puede eliminar: el curso tiene pagos asociados.', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('productos'))


# ------------------- MÓDULO CLIENTES (Estudiantes) -------------------

@app.route('/clientes')
@login_required
def clientes():
    """Muestra los estudiantes registrados, recuperados desde PostgreSQL.
    Ruta protegida."""
    conn = get_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute('SELECT * FROM estudiantes ORDER BY id_estudiante DESC')
    estudiantes = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('clientes.html', estudiantes=estudiantes)


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_cliente():
    """Formulario de registro de un estudiante, validado con Flask-WTF
    y almacenado mediante INSERT en PostgreSQL. Ruta protegida."""
    form = EstudianteForm()

    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO estudiantes (nombre, cedula, telefono, correo)
               VALUES (%s, %s, %s, %s)''',
            (form.nombre.data, form.cedula.data, form.telefono.data, form.correo.data)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash(f'Estudiante "{form.nombre.data}" registrado correctamente.', 'success')
        return redirect(url_for('clientes'))

    return render_template('formulario_cliente.html', form=form, modo='nuevo')


@app.route('/clientes/editar/<int:id_estudiante>', methods=['GET', 'POST'])
@login_required
def editar_cliente(id_estudiante):
    """Recupera un estudiante por su identificador, permite editarlo y
    guarda los cambios mediante UPDATE ... WHERE id_estudiante = %s.
    Ruta protegida."""
    conn = get_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute('SELECT * FROM estudiantes WHERE id_estudiante = %s', (id_estudiante,))
    estudiante = cursor.fetchone()
    cursor.close()

    if estudiante is None:
        conn.close()
        flash('El estudiante solicitado no existe.', 'danger')
        return redirect(url_for('clientes'))

    form = EstudianteForm(data=estudiante) if request.method == 'GET' else EstudianteForm()

    if form.validate_on_submit():
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE estudiantes
               SET nombre = %s, cedula = %s, telefono = %s, correo = %s
               WHERE id_estudiante = %s''',
            (form.nombre.data, form.cedula.data, form.telefono.data,
             form.correo.data, id_estudiante)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash(f'Estudiante "{form.nombre.data}" actualizado correctamente.', 'success')
        return redirect(url_for('clientes'))

    conn.close()
    return render_template('formulario_cliente.html', form=form, modo='editar', id_estudiante=id_estudiante)


@app.route('/clientes/eliminar/<int:id_estudiante>', methods=['POST'])
@login_required
def eliminar_cliente(id_estudiante):
    """Elimina únicamente el estudiante seleccionado. Ruta protegida.

    Nota: si el estudiante tiene pagos asociados, PostgreSQL rechazará el
    DELETE por la FOREIGN KEY de pagos.id_estudiante (integridad
    referencial); en ese caso se informa el error al usuario."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM estudiantes WHERE id_estudiante = %s', (id_estudiante,))
        conn.commit()
        flash('Estudiante eliminado correctamente.', 'success')
    except Exception:
        conn.rollback()
        flash('No se puede eliminar: el estudiante tiene pagos asociados.', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('clientes'))


# ------------------- MÓDULO PROVEEDORES (Instructores) -------------------

@app.route('/proveedores')
@login_required
def proveedores():
    """Muestra los instructores de la plataforma, recuperados desde
    PostgreSQL. Ruta protegida."""
    conn = get_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute('SELECT * FROM instructores ORDER BY id_instructor DESC')
    instructores = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('proveedores.html', instructores=instructores)


@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_proveedor():
    """Formulario de registro de un instructor, validado con Flask-WTF
    y almacenado mediante INSERT en PostgreSQL. Ruta protegida."""
    form = InstructorForm()

    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO instructores (nombre, especialidad, correo)
               VALUES (%s, %s, %s)''',
            (form.nombre.data, form.especialidad.data, form.correo.data)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash(f'Instructor "{form.nombre.data}" registrado correctamente.', 'success')
        return redirect(url_for('proveedores'))

    return render_template('formulario_proveedor.html', form=form, modo='nuevo')


@app.route('/proveedores/editar/<int:id_instructor>', methods=['GET', 'POST'])
@login_required
def editar_proveedor(id_instructor):
    """Recupera un instructor por su identificador, permite editarlo y
    guarda los cambios mediante UPDATE ... WHERE id_instructor = %s.
    Ruta protegida."""
    conn = get_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute('SELECT * FROM instructores WHERE id_instructor = %s', (id_instructor,))
    instructor = cursor.fetchone()
    cursor.close()

    if instructor is None:
        conn.close()
        flash('El instructor solicitado no existe.', 'danger')
        return redirect(url_for('proveedores'))

    form = InstructorForm(data=instructor) if request.method == 'GET' else InstructorForm()

    if form.validate_on_submit():
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE instructores
               SET nombre = %s, especialidad = %s, correo = %s
               WHERE id_instructor = %s''',
            (form.nombre.data, form.especialidad.data, form.correo.data, id_instructor)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash(f'Instructor "{form.nombre.data}" actualizado correctamente.', 'success')
        return redirect(url_for('proveedores'))

    conn.close()
    return render_template('formulario_proveedor.html', form=form, modo='editar', id_instructor=id_instructor)


@app.route('/proveedores/eliminar/<int:id_instructor>', methods=['POST'])
@login_required
def eliminar_proveedor(id_instructor):
    """Elimina únicamente el instructor seleccionado. Ruta protegida.

    Nota: si el instructor dicta algún curso, PostgreSQL rechazará el
    DELETE por la FOREIGN KEY de cursos.id_instructor (integridad
    referencial); en ese caso se informa el error al usuario en vez de
    dejar cursos "huérfanos"."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM instructores WHERE id_instructor = %s', (id_instructor,))
        conn.commit()
        flash('Instructor eliminado correctamente.', 'success')
    except Exception:
        conn.rollback()
        flash('No se puede eliminar: el instructor tiene cursos asociados.', 'danger')
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('proveedores'))


# ------------------- MÓDULO FACTURACIÓN (Pagos) -------------------

def obtener_choices_estudiantes():
    """Consulta los estudiantes en PostgreSQL y arma la lista de choices
    (id_estudiante, nombre) para el SelectField del formulario de pagos."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id_estudiante, nombre FROM estudiantes ORDER BY nombre')
    estudiantes = cursor.fetchall()
    cursor.close()
    conn.close()
    return [(id_estudiante, nombre) for (id_estudiante, nombre) in estudiantes]


def obtener_choices_cursos():
    """Consulta los cursos en PostgreSQL y arma la lista de choices
    (id_curso, nombre) para el SelectField del formulario de pagos."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id_curso, nombre FROM cursos ORDER BY nombre')
    cursos = cursor.fetchall()
    cursor.close()
    conn.close()
    return [(id_curso, nombre) for (id_curso, nombre) in cursos]


@app.route('/facturacion')
@login_required
def facturacion():
    """Muestra los pagos/matrículas registrados, recuperados desde
    PostgreSQL mediante un JOIN con estudiantes y cursos para mostrar
    sus nombres en lugar de solo el id. Ruta protegida."""
    conn = get_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute('''
        SELECT p.id_pago, p.monto, p.fecha,
               e.id_estudiante, e.nombre AS estudiante,
               c.id_curso, c.nombre AS curso
        FROM pagos p
        JOIN estudiantes e ON p.id_estudiante = e.id_estudiante
        JOIN cursos c ON p.id_curso = c.id_curso
        ORDER BY p.id_pago DESC
    ''')
    pagos = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('facturacion.html', pagos=pagos)


@app.route('/facturacion/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_pago():
    """Formulario de registro de un pago, validado con Flask-WTF y
    almacenado mediante INSERT en PostgreSQL. Ruta protegida."""
    form = PagoForm()
    form.id_estudiante.choices = obtener_choices_estudiantes()
    form.id_curso.choices = obtener_choices_cursos()

    if form.validate_on_submit():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO pagos (id_estudiante, id_curso, monto, fecha)
               VALUES (%s, %s, %s, %s)''',
            (form.id_estudiante.data, form.id_curso.data, form.monto.data, form.fecha.data)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Pago registrado correctamente.', 'success')
        return redirect(url_for('facturacion'))

    return render_template('formulario_facturacion.html', form=form, modo='nuevo')


@app.route('/facturacion/editar/<int:id_pago>', methods=['GET', 'POST'])
@login_required
def editar_pago(id_pago):
    """Recupera un pago por su identificador, permite editarlo y guarda
    los cambios mediante UPDATE ... WHERE id_pago = %s. Ruta protegida."""
    conn = get_connection()
    cursor = get_dict_cursor(conn)
    cursor.execute('SELECT * FROM pagos WHERE id_pago = %s', (id_pago,))
    pago = cursor.fetchone()
    cursor.close()

    if pago is None:
        conn.close()
        flash('El pago solicitado no existe.', 'danger')
        return redirect(url_for('facturacion'))

    form = PagoForm(data=pago) if request.method == 'GET' else PagoForm()
    form.id_estudiante.choices = obtener_choices_estudiantes()
    form.id_curso.choices = obtener_choices_cursos()

    if form.validate_on_submit():
        cursor = conn.cursor()
        cursor.execute(
            '''UPDATE pagos
               SET id_estudiante = %s, id_curso = %s, monto = %s, fecha = %s
               WHERE id_pago = %s''',
            (form.id_estudiante.data, form.id_curso.data, form.monto.data,
             form.fecha.data, id_pago)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Pago actualizado correctamente.', 'success')
        return redirect(url_for('facturacion'))

    conn.close()
    return render_template('formulario_facturacion.html', form=form, modo='editar', id_pago=id_pago)


@app.route('/facturacion/eliminar/<int:id_pago>', methods=['POST'])
@login_required
def eliminar_pago(id_pago):
    """Elimina únicamente el pago seleccionado. Ruta protegida."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pagos WHERE id_pago = %s', (id_pago,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Pago eliminado correctamente.', 'success')
    return redirect(url_for('facturacion'))


if __name__ == '__main__':
    app.run(debug=True)
