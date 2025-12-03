from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from datetime import datetime
from models import Usuario, Organizador
import re

class CadastroUnificadoForm(FlaskForm):
    tipo = SelectField('Tipo de Cadastro', 
                      choices=[('usuario', 'Usuário'), ('organizador', 'Organizador')],
                      validators=[DataRequired()])
    nome = StringField('Nome Completo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    usuario = StringField('Nome de Usuário', validators=[Optional()])
    cpf = StringField('CPF', validators=[Optional()])

    cpf_cnpj = StringField('CPF/CNPJ', validators=[Optional()])

    telefone = StringField('Telefone', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirma_senha = PasswordField('Confirmar Senha', 
                                  validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Criar Conta')
    
    def validate(self, extra_validators=None):
        if not super().validate():
            return False

        if self.tipo.data == 'usuario':
            if not self.usuario.data:
                self.usuario.errors = ['Nome de usuário é obrigatório para usuários']
                return False
            if not self.cpf.data:
                self.cpf.errors = ['CPF é obrigatório para usuários']
                return False

            user = Usuario.query.filter_by(nome_usuario=self.usuario.data).first()
            if user:
                self.usuario.errors = ['Nome de usuário já está em uso.']
                return False

            user = Usuario.query.filter_by(CPF=self.cpf.data).first()
            if user:
                self.cpf.errors = ['CPF já está cadastrado.']
                return False
        
        elif self.tipo.data == 'organizador':
            if not self.cpf_cnpj.data:
                self.cpf_cnpj.errors = ['CPF/CNPJ é obrigatório para organizadores']
                return False

            org = Organizador.query.filter_by(cpf_cnpj=self.cpf_cnpj.data).first()
            if org:
                self.cpf_cnpj.errors = ['CPF/CNPJ já está cadastrado.']
                return False

        if self.tipo.data == 'usuario':
            user = Usuario.query.filter_by(email=self.email.data).first()
            if user:
                self.email.errors = ['Email já está cadastrado.']
                return False
        else:
            org = Organizador.query.filter_by(email=self.email.data).first()
            if org:
                self.email.errors = ['Email já está cadastrado.']
                return False
        
        return True

class LoginUnificadoForm(FlaskForm):
    usuario = StringField('Usuário ou Email', validators=[DataRequired()], 
                         render_kw={"placeholder": "Digite seu usuário ou email"})
    senha = PasswordField('Senha', validators=[DataRequired()],
                         render_kw={"placeholder": "Digite sua senha"})
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

class AtividadeForm(FlaskForm):
    titulo = StringField('Título da Atividade', validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    data = DateField('Data da Atividade', validators=[DataRequired()], format='%Y-%m-%d')
    horario_inicio = TimeField('Horário de Início', validators=[DataRequired()], format='%H:%M')
    horario_fim = TimeField('Horário de Término', validators=[DataRequired()], format='%H:%M')
    convidado = StringField('Convidado/Palestrante', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Adicionar Atividade')
    
    def validate_data(self, field):
        if field.data < datetime.now().date():
            raise ValidationError('A data da atividade não pode ser no passado.')
    
    def validate_horario_fim(self, field):
        if self.horario_inicio.data and field.data:
            if field.data <= self.horario_inicio.data:
                raise ValidationError('O horário de término deve ser após o horário de início.')