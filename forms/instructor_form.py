"""
forms/instructor_form.py
Formulario del módulo Proveedores (Instructores), basado en Flask-WTF y WTForms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class InstructorForm(FlaskForm):
    """Formulario para registrar o editar un instructor."""

    nombre = StringField(
        'Nombre completo',
        validators=[DataRequired(message='El nombre es obligatorio.'),
                    Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres.')]
    )

    especialidad = StringField(
        'Especialidad',
        validators=[DataRequired(message='La especialidad es obligatoria.'),
                    Length(min=3, max=100, message='La especialidad debe tener entre 3 y 100 caracteres.')]
    )

    correo = StringField(
        'Correo electrónico',
        validators=[DataRequired(message='El correo es obligatorio.'),
                    Email(message='Ingrese un correo electrónico válido.')]
    )

    submit = SubmitField('Guardar instructor')
