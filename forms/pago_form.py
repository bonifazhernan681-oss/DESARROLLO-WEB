"""
forms/pago_form.py
Formulario del módulo Facturación (Pagos), basado en Flask-WTF y WTForms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class PagoForm(FlaskForm):
    """Formulario para registrar o editar un pago/matrícula."""

    numero = StringField(
        'N° de factura',
        validators=[DataRequired(message='El número de factura es obligatorio.'),
                    Length(min=3, max=20, message='El número de factura debe tener entre 3 y 20 caracteres.')]
    )

    estudiante = StringField(
        'Estudiante',
        validators=[DataRequired(message='El nombre del estudiante es obligatorio.'),
                    Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres.')]
    )

    curso = StringField(
        'Curso',
        validators=[DataRequired(message='El curso es obligatorio.'),
                    Length(min=3, max=100, message='El curso debe tener entre 3 y 100 caracteres.')]
    )

    monto = FloatField(
        'Monto ($)',
        validators=[DataRequired(message='El monto es obligatorio.'),
                    NumberRange(min=0, message='El monto no puede ser negativo.')]
    )

    fecha = DateField(
        'Fecha de pago',
        format='%d/%m/%Y',
        validators=[DataRequired(message='La fecha de pago es obligatoria.')]
    )

    submit = SubmitField('Guardar pago')
