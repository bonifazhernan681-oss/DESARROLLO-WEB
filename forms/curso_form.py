"""
forms/curso_form.py
Formulario del módulo Productos (Cursos), basado en Flask-WTF y WTForms.

Semana 13: se agrega el campo id_instructor (SelectField) para poder
registrar la relación de clave foránea cursos.id_instructor ->
instructores.id_instructor. Sus choices se cargan dinámicamente desde
la base de datos en app.py antes de validar el formulario.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class CursoForm(FlaskForm):
    """Formulario para registrar o editar un curso del catálogo."""

    nombre = StringField(
        'Nombre del curso',
        validators=[DataRequired(message='El nombre del curso es obligatorio.'),
                    Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres.')]
    )

    descripcion = TextAreaField(
        'Descripción',
        validators=[DataRequired(message='La descripción es obligatoria.'),
                    Length(min=10, max=300, message='La descripción debe tener entre 10 y 300 caracteres.')]
    )

    categoria = SelectField(
        'Categoría',
        choices=[
            ('Frontend', 'Frontend'),
            ('Backend', 'Backend'),
            ('Base de Datos', 'Base de Datos'),
            ('DevOps', 'DevOps'),
        ],
        validators=[DataRequired(message='Seleccione una categoría.')]
    )

    precio = FloatField(
        'Precio ($)',
        validators=[DataRequired(message='El precio es obligatorio.'),
                    NumberRange(min=0, message='El precio no puede ser negativo.')]
    )

    cupos = IntegerField(
        'Cupos disponibles',
        validators=[DataRequired(message='El número de cupos es obligatorio.'),
                    NumberRange(min=0, message='Los cupos no pueden ser negativos.')]
    )

    id_instructor = SelectField(
        'Instructor',
        coerce=int,
        validators=[DataRequired(message='Seleccione un instructor.')]
    )

    submit = SubmitField('Guardar curso')
