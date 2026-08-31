"""
forms/curso_form.py
Formulario del módulo Productos (Cursos), basado en Flask-WTF y WTForms.
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

    submit = SubmitField('Guardar curso')
