from wtforms import Form, SubmitField, IntegerField,FloatField, StringField,TextAreaField, validators, PasswordField, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import FlaskForm
from .models import Cadastrar

class CadastroClienteForm(FlaskForm):
    name = StringField('Nome : ',[validators.DataRequired()])
    username = StringField('Usuario : ',[validators.DataRequired()])
    email = StringField('Email : ',[validators.DataRequired()])
    password = PasswordField('Senha:', [validators.DataRequired(), validators.EqualTo('confirm', message='As duas senhas devem ser iguais!')])
    confirm = PasswordField('Redigite Senha : ',[validators.DataRequired()])
    country = StringField('Pais : ',[validators.DataRequired()])
    city = StringField('Cidade : ',[validators.DataRequired()])
    contact = StringField('Contato : ',[validators.DataRequired()])
    address = StringField('Endereco : ',[validators.DataRequired()])
    zipcode = StringField('CEP : ',[validators.DataRequired()])
    profile = FileField('Perfil', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])

    submit = SubmitField('Cadastrar')


    def validate_username(self, username):
        if Cadastrar.query.filter_by(username=username.data).first():
            raise ValidationError("Este Usuario ja esta em uso")
    
    def validate_email(self, email):
        if Cadastrar.query.filter_by(email=email.data).first():
            raise ValidationError("Este E-mail ja esta em uso")