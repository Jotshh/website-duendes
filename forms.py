from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import Usuario, Organizador

class CadastroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    usuario = StringField('Usuário', validators=[DataRequired(), Length(min=3, max=50)])
    cpf = StringField('CPF', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirma_senha = PasswordField('Confirmar Senha', 
                                 validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Criar Conta')
    
    def validate_usuario(self, usuario):
        user = Usuario.query.filter_by(nome_usuario=usuario.data).first()
        if user:
            raise ValidationError('Nome de usuário já está em uso.')
    
    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email já está cadastrado.')
    
    def validate_cpf(self, cpf):
        user = Usuario.query.filter_by(CPF=cpf.data).first()
        if user:
            raise ValidationError('CPF já está cadastrado.')

class LoginForm(FlaskForm):
    usuario = StringField('Usuário ou Email', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    tipo = SelectField('Tipo de Login', 
                      choices=[('usuario', 'Usuário'), ('organizador', 'Organizador')],
                      validators=[DataRequired()])
    submit = SubmitField('Entrar')