"""
forms/usuario_form.py
Formularios de Registro e Inicio de Sesión, basados en Flask-WTF y WTForms.
Semana 14: sistema de autenticación.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistroForm(FlaskForm):
    """Formulario para registrar un nuevo usuario del sistema."""

    usuario = StringField(
        'Usuario',
        validators=[DataRequired(message='El usuario es obligatorio.'),
                    Length(min=4, max=50, message='El usuario debe tener entre 4 y 50 caracteres.')]
    )

    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(message='La contraseña es obligatoria.'),
                    Length(min=6, message='La contraseña debe tener al menos 6 caracteres.')]
    )

    confirmar_password = PasswordField(
        'Confirmar contraseña',
        validators=[DataRequired(message='Debe confirmar la contraseña.'),
                    EqualTo('password', message='Las contraseñas no coinciden.')]
    )

    submit = SubmitField('Registrarse')


class LoginForm(FlaskForm):
    """Formulario de inicio de sesión."""

    usuario = StringField(
        'Usuario',
        validators=[DataRequired(message='El usuario es obligatorio.')]
    )

    password = PasswordField(
        'Contraseña',
        validators=[DataRequired(message='La contraseña es obligatoria.')]
    )

    submit = SubmitField('Iniciar sesión')
