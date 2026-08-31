"""
forms/estudiante_form.py
Formulario del módulo Clientes (Estudiantes), basado en Flask-WTF y WTForms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class EstudianteForm(FlaskForm):
    """Formulario para registrar o editar un estudiante."""

    nombre = StringField(
        'Nombre completo',
        validators=[DataRequired(message='El nombre es obligatorio.'),
                    Length(min=3, max=100, message='El nombre debe tener entre 3 y 100 caracteres.')]
    )

    correo = StringField(
        'Correo electrónico',
        validators=[DataRequired(message='El correo es obligatorio.'),
                    Email(message='Ingrese un correo electrónico válido.')]
    )

    curso = StringField(
        'Curso inscrito',
        validators=[DataRequired(message='Indique el curso en el que se inscribe.'),
                    Length(min=3, max=100, message='El curso debe tener entre 3 y 100 caracteres.')]
    )

    estado = SelectField(
        'Estado',
        choices=[
            ('Activo', 'Activo'),
            ('Inactivo', 'Inactivo'),
        ],
        validators=[DataRequired(message='Seleccione un estado.')]
    )

    submit = SubmitField('Guardar estudiante')
