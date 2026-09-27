"""
forms/estudiante_form.py
Formulario del módulo Clientes (Estudiantes), basado en Flask-WTF y WTForms.

Semana 15: los campos se alinean con las columnas reales de la tabla
estudiantes en PostgreSQL (nombre, cedula, telefono, correo).
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional


class EstudianteForm(FlaskForm):
    """Formulario para registrar o editar un estudiante."""

    nombre = StringField(
        'Nombre completo',
        validators=[DataRequired(message='El nombre es obligatorio.'),
                    Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres.')]
    )

    cedula = StringField(
        'Cédula',
        validators=[DataRequired(message='La cédula es obligatoria.'),
                    Length(min=10, max=20, message='La cédula debe tener entre 10 y 20 caracteres.')]
    )

    telefono = StringField(
        'Teléfono',
        validators=[Optional(),
                    Length(max=20, message='El teléfono no puede superar los 20 caracteres.')]
    )

    correo = StringField(
        'Correo electrónico',
        validators=[DataRequired(message='El correo es obligatorio.'),
                    Email(message='Ingrese un correo electrónico válido.')]
    )

    submit = SubmitField('Guardar estudiante')
