"""
forms/pago_form.py
Formulario del módulo Facturación (Pagos), basado en Flask-WTF y WTForms.

Semana 15: id_estudiante e id_curso pasan a ser SelectField (claves
foráneas reales hacia estudiantes y cursos), alineados con la tabla
pagos en PostgreSQL. Sus choices se cargan dinámicamente desde la base
de datos en app.py antes de validar el formulario.
"""

from flask_wtf import FlaskForm
from wtforms import SelectField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class PagoForm(FlaskForm):
    """Formulario para registrar o editar un pago/matrícula."""

    id_estudiante = SelectField(
        'Estudiante',
        coerce=int,
        validators=[DataRequired(message='Seleccione un estudiante.')]
    )

    id_curso = SelectField(
        'Curso',
        coerce=int,
        validators=[DataRequired(message='Seleccione un curso.')]
    )

    monto = FloatField(
        'Monto ($)',
        validators=[DataRequired(message='El monto es obligatorio.'),
                    NumberRange(min=0, message='El monto no puede ser negativo.')]
    )

    fecha = DateField(
        'Fecha de pago',
        format='%Y-%m-%d',
        validators=[DataRequired(message='La fecha de pago es obligatoria.')]
    )

    submit = SubmitField('Guardar pago')
