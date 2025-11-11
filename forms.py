from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from datetime import datetime
from models import Usuario, Organizador
import re

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

class EventoForm(FlaskForm):
    titulo = StringField('Título do Evento', validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    local = StringField('Local', validators=[DataRequired(), Length(max=100)])
    data = DateField('Data do Evento', validators=[DataRequired()], format='%Y-%m-%d')
    horario = TimeField('Horário', validators=[DataRequired()], format='%H:%M')
    categoria = SelectField('Categoria', 
                          choices=[
                              ('festas', 'Festas'),
                              ('shows', 'Shows'),
                              ('esportes', 'Esportes'),
                              ('tecnologia', 'Tecnologia'),
                              ('academico', 'Acadêmico'),
                              ('cultural', 'Cultural'),
                              ('workshop', 'Workshop'),
                              ('outros', 'Outros')
                          ],
                          validators=[DataRequired()])
    imagem_url = StringField('URL da Imagem (opcional)')
    submit = SubmitField('Criar Evento')
    
    def validate_data(self, field):
        if field.data < datetime.now().date():
            raise ValidationError('A data do evento não pode ser no passado.') 