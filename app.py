from flask import Flask, request, render_template, redirect, jsonify, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, g 
import functools

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'teste'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/bd_duendes_site'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, server_default=db.func.now())
    
    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)
    
    def check_senha(self, senha):
        return check_password_hash(self.senha, senha)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'usuario': self.usuario,
            'email': self.email
        }

class CadastroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    usuario = StringField('Usuário', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirma_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])

#DEFININDO A FUNCAO DE LOGIN NECESSARIO
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('entrar'))
        return view(**kwargs)
    return wrapped_view

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = Usuario.query.get(user_id)

@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    
    if form.validate_on_submit():
        try:
            # Verifica se usuário existe
            if Usuario.query.filter_by(usuario=form.usuario.data).first():
                flash('Nome de usuário já está em uso', 'error')
                return render_template("cadastro.html", form=form)
            
            # Verifica se email existe
            if Usuario.query.filter_by(email=form.email.data).first():
                flash('Email já está cadastrado', 'error')
                return render_template("cadastro.html", form=form)
            
            # Verifica o CPF 
            if Usuario.query.filter_by(cpf=form.cpf.data).first():
                flash('CPF já está cadastrado', 'error')
                return render_template("cadastro.html", form=form)
            
            # Cria novo usuário
            novo_usuario = Usuario(
                nome=form.nome.data,
                usuario=form.usuario.data,
                cpf=form.cpf.data,
                telefone=form.telefone.data,
                email=form.email.data
            )
            novo_usuario.set_senha(form.senha.data)
            
            db.session.add(novo_usuario)
            db.session.commit()
            
            flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('entrar'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao realizar cadastro. Tente novamente.', 'error')
            print(f"Erro: {e}")
    
    return render_template("cadastro.html", form=form)

@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    if request.method == 'POST':
        usuario_input = request.form.get('usuario')  
        senha_input = request.form.get('senha')
        
        usuario = Usuario.query.filter_by(usuario=usuario_input).first()
        
        if usuario:
            print(f"✅ Usuário encontrado: {usuario.usuario}")
            if usuario.check_senha(senha_input):
                session.clear()
                session['user_id'] = usuario.id
                print(f"🎉 Login bem-sucedido! id do usuário: {usuario.id}")
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('perfil'))
            else:
                print("❌ Senha incorreta")
                flash('Senha incorreta', 'error')
        else:
            print("❌ Usuário não encontrado")
            flash('Usuário não encontrado', 'error')
    
    return render_template("entrar.html")

# Rota de logout
@app.route('/sair')
def sair():
    session.clear()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('inicio'))

# Rota do perfil
@app.route('/perfil')
@login_required
def perfil():
    return render_template("perfil.html", usuario=g.user)

# Rota para editar perfil
@app.route('/editar-perfil', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'POST':
        try:
            usuario = g.user
            usuario.nome = request.form.get('nome')
            usuario.telefone = request.form.get('telefone')
            usuario.email = request.form.get('email')
            
            db.session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('perfil'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar perfil.', 'error')
    
    return render_template("editar_perfil.html", usuario=g.user)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5152)