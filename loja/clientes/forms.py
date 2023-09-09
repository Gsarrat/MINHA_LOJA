from wtforms import Form, SubmitField, IntegerField,FloatField, StringField,TextAreaField, validators, PasswordField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class CadastroClienteForm(Form):
    name = StringField('Nome : ')
    username = StringField('Usuario : ',[validators.DataRequired()])
    email = StringField('Email : ',[validators.DataRequired()])
    password = PasswordField('Senha:', [validators.DataRequired(), validators.EqualTo('confirm', message='As duas senhas devem ser iguais!')])
    confirm = PasswordField('Redigite Senha : ',[validators.DataRequired()])
    country = StringField('Pais : ',[validators.DataRequired()])
    state = StringField('Estado : ',[validators.DataRequired()])
    city = StringField('Cidade : ',[validators.DataRequired()])
    contact = StringField('Contato : ',[validators.DataRequired()])
    address = StringField('Endereco : ',[validators.DataRequired()])
    zipcode = StringField('CEP : ',[validators.DataRequired()])
    profile = FileField('Perfil', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])

    submit = SubmitField('Cadastrar')