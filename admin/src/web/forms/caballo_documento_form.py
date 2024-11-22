from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed

class CaballoDocumentoForm(FlaskForm):
    titulo = StringField('Título del Documento', validators=[
        DataRequired(),
        Length(min=2, max=255)
    ])

    tipo_documento = SelectField('Tipo de Documento', choices=[
        ('ficha', 'Ficha general del caballo'),
        ('planificacion', 'Planificación de Entrenamiento'),
        ('informe', 'Informe de Evolución'),
        ('imagenes', 'Carga de Imágenes'),
        ('veterinario', 'Registro Veterinario')
    ], validators=[DataRequired()])
    
    archivo = FileField('Archivo', validators=[
        DataRequired(),
        FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Solo se permiten archivos PDF o imágenes (JPG, PNG)')
    ])

    submit = SubmitField('Subir Documento')
