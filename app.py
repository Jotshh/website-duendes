from flask import Flask, request, render_template, redirect, jsonify, flash, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
from models import db, Usuario, Organizador
from forms import CadastroForm, LoginForm
import functools

app = Flask(__name__)
app.config['SECRET_KEY'] = 'teste'  

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/bd_duendes_site'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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
    user_type = session.get('user_type')
    
    if user_id is None:
        g.user = None
    else:
        if user_type == 'usuario':
            g.user = Usuario.query.get(user_id)
        elif user_type == 'organizador':
            g.user = Organizador.query.get(user_id)

@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    
    if form.validate_on_submit():
        try:
            
            novo_usuario = Usuario(
                nome=form.nome.data,
                nome_usuario=form.usuario.data,
                CPF=form.cpf.data,
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
    
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'error')
    
    return render_template("cadastro.html", form=form)

@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    form = LoginForm()
    
    if form.validate_on_submit():
        usuario_input = form.usuario.data
        senha_input = form.senha.data
        tipo_input = form.tipo.data
        
        print(f"🔐 Tentando login: {usuario_input}, tipo: {tipo_input}")  # Debug
        
        if tipo_input == 'usuario':
            
            usuario = Usuario.query.filter(
                (Usuario.nome_usuario == usuario_input) | (Usuario.email == usuario_input)
            ).first()
            
            if usuario:
                print(f"✅ Usuário encontrado: {usuario.nome_usuario}")
                if usuario.check_senha(senha_input):
                    session.clear()
                    session['user_id'] = usuario.ID
                    session['user_type'] = 'usuario'
                    flash('Login realizado com sucesso!', 'success')
                    return redirect(url_for('perfil'))
                else:
                    print("❌ Senha incorreta")
                    flash('Senha incorreta', 'error')
            else:
                print("❌ Usuário não encontrado")
                flash('Usuário não encontrado', 'error')
        
        elif tipo_input == 'organizador':
            organizador = Organizador.query.filter_by(email=usuario_input).first()
            if organizador:
                print(f"✅ Organizador encontrado: {organizador.nome}")
                if organizador.check_senha(senha_input):
                    session.clear()
                    session['user_id'] = organizador.ID
                    session['user_type'] = 'organizador'
                    flash('Login como organizador realizado com sucesso!', 'success')
                    return redirect(url_for('dashboard_organizador'))
                else:
                    flash('Senha incorreta', 'error')
            else:
                flash('Organizador não encontrado', 'error')
    
    return render_template("entrar.html", form=form)

@app.route('/sair')
def sair():
    session.clear()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('inicio'))

@app.route('/perfil')
@login_required
def perfil():
    
    if session.get('user_type') != 'usuario':
        flash('Acesso não autorizado.', 'error')
        return redirect(url_for('inicio'))
    
    usuario = Usuario.query.get(session['user_id'])
    if not usuario:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('entrar'))
    
    return render_template("perfil.html", usuario=usuario)

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

@app.route('/dashboard-organizador')
@login_required
def dashboard_organizador():
    if session.get('user_type') != 'organizador':
        flash('Acesso não autorizado.', 'error')
        return redirect(url_for('inicio'))
    return "Dashboard do Organizador - Em desenvolvimento"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5152)