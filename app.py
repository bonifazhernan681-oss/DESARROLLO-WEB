"""
app.py
Proyecto Integrador U3 - Avance 9/16
Configuración de un proyecto web con Flask y manejo de rutas.

Este archivo convierte la página estática desarrollada en semanas
anteriores en una aplicación Flask, con rutas para cada módulo del
sistema. En esta etapa no se usa base de datos: los datos que se
muestran en cada módulo son de ejemplo (listas de Python).
"""

from flask import Flask, render_template

app = Flask(__name__)


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
            'precio': '$25.00'
        },
        {
            'nombre': 'CSS3 y diseño responsive',
            'descripcion': 'Estilos, Flexbox, Grid y adaptabilidad a dispositivos.',
            'categoria': 'Frontend',
            'precio': '$30.00'
        },
        {
            'nombre': 'JavaScript desde cero',
            'descripcion': 'Lógica de programación aplicada al navegador.',
            'categoria': 'Frontend',
            'precio': '$35.00'
        },
        {
            'nombre': 'Python con Flask',
            'descripcion': 'Desarrollo de aplicaciones web con Python.',
            'categoria': 'Backend',
            'precio': '$40.00'
        },
        {
            'nombre': 'Bases de datos relacionales',
            'descripcion': 'Modelado ER, SQL y administración de datos.',
            'categoria': 'Base de Datos',
            'precio': '$35.00'
        },
        {
            'nombre': 'Despliegue en la nube',
            'descripcion': 'Publicación y escalado de aplicaciones web.',
            'categoria': 'DevOps',
            'precio': '$45.00'
        },
    ]
    return render_template('productos.html', cursos=cursos)


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


if __name__ == '__main__':
    app.run(debug=True)
