from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

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