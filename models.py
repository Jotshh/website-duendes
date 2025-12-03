from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()
class Usuario(db.Model):
    __tablename__ = 'Usuario' 
    
    ID = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    CPF = db.Column(db.String(14), unique=True, nullable=False)
    nome_usuario = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    tipo_usuario = db.Column(db.String(20), nullable=False, default='participante')
    telefone = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.TIMESTAMP, server_default=db.func.now())
    
    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)
    
    def check_senha(self, senha):
        return check_password_hash(self.senha, senha)
    
    def to_dict(self):
        return {
            'id': self.ID,
            'nome': self.nome,
            'nome_usuario': self.nome_usuario,
            'email': self.email,
            'telefone': self.telefone,
            'cpf': self.CPF,
            'data_criacao': self.data_criacao
        }

class Organizador(db.Model):
    __tablename__ = 'Organizador'
    
    ID = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cpf_cnpj = db.Column(db.String(20), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.TIMESTAMP, server_default=db.func.now())
    
    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)
    
    def check_senha(self, senha):
        return check_password_hash(self.senha, senha)


class Evento(db.Model):
    __tablename__ = 'Evento'
    
    ID = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    local = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Date, nullable=False)
    horario = db.Column(db.Time, nullable=False)
    categoria = db.Column(db.String(45), nullable=False)
    Organizador_ID = db.Column(db.Integer, db.ForeignKey('Organizador.ID'), nullable=False)
    imagem_url = db.Column(db.String(255))
    data_criacao = db.Column(db.TIMESTAMP, server_default=db.func.now())

    organizador = db.relationship('Organizador', backref='eventos')
    
    def to_dict(self):
        return {
            'id': self.ID,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'local': self.local,
            'data': self.data.isoformat() if self.data else None,
            'horario': self.horario.strftime('%H:%M') if self.horario else None,
            'categoria': self.categoria,
            'organizador_id': self.Organizador_ID,
            'organizador_nome': self.organizador.nome if self.organizador else '',
            'imagem_url': self.imagem_url,
            'data_criacao': self.data_criacao
        }
    
#CRIAR CLASSE ATIVIDADES
class Atividades(db.Model):
    __tablename__ = 'Atividades'
    
    ID = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data = db.Column(db.Date, nullable=False)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    convidado = db.Column(db.String(100), nullable=False)
    Evento_ID = db.Column(db.Integer, db.ForeignKey('Evento.ID'), nullable=False)
    data_criacao = db.Column(db.TIMESTAMP, server_default=db.func.now())
    
    evento = db.relationship('Evento', backref='atividades')
    
    def to_dict(self):
        return {
            'id': self.ID,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'data': self.data.isoformat() if self.data else None,
            'horario_inicio': self.horario_inicio.strftime('%H:%M') if self.horario_inicio else None,
            'horario_fim': self.horario_fim.strftime('%H:%M') if self.horario_fim else None,
            'convidado': self.convidado,
            'evento_id': self.Evento_ID,
            'data_criacao': self.data_criacao
        }

#CRIAR CLASSE INSCRICAO
class Inscricao(db.Model):
    __tablename__ = 'Inscricao_Evento'
    
    ID = db.Column(db.Integer, primary_key=True)
    Usuario_ID = db.Column(db.Integer, db.ForeignKey('Usuario.ID'), nullable=False)
    Evento_ID = db.Column(db.Integer, db.ForeignKey('Evento.ID'), nullable=False)
    data_inscricao = db.Column(db.TIMESTAMP, server_default=db.func.now())
    status = db.Column(db.String(20), nullable=False, default='confirmada')
    
    usuario = db.relationship('Usuario', backref='inscricoes')
    evento = db.relationship('Evento', backref='inscricoes')
    
    def to_dict(self):
        return {
            'id': self.ID,
            'usuario_id': self.Usuario_ID,
            'evento_id': self.Evento_ID,
            'data_inscricao': self.data_inscricao,
            'status': self.status
        }      