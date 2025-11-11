from flask import Flask, request, render_template, redirect, jsonify, flash, url_for, session, g
from flask_sqlalchemy import SQLAlchemy
from models import db, Usuario, Organizador, Evento, Inscricao
from forms import CadastroForm, LoginForm, EventoForm 
import functools
from datetime import datetime

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

@app.route('/criar-evento', methods=['GET', 'POST'])
@login_required
def criar_evento():
    # Verificar se o usuário é um organizador
    if session.get('user_type') != 'organizador':
        flash('Apenas organizadores podem criar eventos.', 'error')
        return redirect(url_for('inicio'))
    
    form = EventoForm()
    
    if form.validate_on_submit():
        try:
            # Criar novo evento
            novo_evento = Evento(
                titulo=form.titulo.data,
                descricao=form.descricao.data,
                local=form.local.data,
                data=form.data.data,
                horario=form.horario.data,
                categoria=form.categoria.data,
                Organizador_ID=session['user_id'],
                imagem_url=form.imagem_url.data or None
            )
            
            db.session.add(novo_evento)
            db.session.commit()
            
            flash('Evento criado com sucesso!', 'success')
            return redirect(url_for('meus_eventos'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar evento. Tente novamente.', 'error')
            print(f"Erro: {e}")
    
    # Mostrar erros de validação
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'error')
    
    return render_template("criar_evento.html", form=form)

@app.route('/meus-eventos')
@login_required
def meus_eventos():
    if session.get('user_type') != 'organizador':
        flash('Apenas organizadores podem acessar esta página.', 'error')
        return redirect(url_for('inicio'))
    
    organizador_id = session['user_id']
    eventos = Evento.query.filter_by(Organizador_ID=organizador_id).order_by(Evento.data.desc()).all()
    
    return render_template("meus_eventos.html", eventos=eventos)

@app.route('/editar-evento/<int:evento_id>', methods=['GET', 'POST'])
@login_required
def editar_evento(evento_id):
    if session.get('user_type') != 'organizador':
        flash('Apenas organizadores podem editar eventos.', 'error')
        return redirect(url_for('inicio'))
    
    evento = Evento.query.get_or_404(evento_id)
    
    # Verificar se o organizador é o dono do evento
    if evento.Organizador_ID != session['user_id']:
        flash('Você não tem permissão para editar este evento.', 'error')
        return redirect(url_for('meus_eventos'))
    
    form = EventoForm(obj=evento)
    
    if form.validate_on_submit():
        try:
            evento.titulo = form.titulo.data
            evento.descricao = form.descricao.data
            evento.local = form.local.data
            evento.data = form.data.data
            evento.horario = form.horario.data
            evento.categoria = form.categoria.data
            evento.imagem_url = form.imagem_url.data or None
            
            db.session.commit()
            flash('Evento atualizado com sucesso!', 'success')
            return redirect(url_for('meus_eventos'))
            
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar evento.', 'error')
            print(f"Erro: {e}")
    
    return render_template("editar_evento.html", form=form, evento=evento)

@app.route('/excluir-evento/<int:evento_id>', methods=['POST'])
@login_required
def excluir_evento(evento_id):
    if session.get('user_type') != 'organizador':
        flash('Apenas organizadores podem excluir eventos.', 'error')
        return redirect(url_for('inicio'))
    
    evento = Evento.query.get_or_404(evento_id)
    
    # Verificar se o organizador é o dono do evento
    if evento.Organizador_ID != session['user_id']:
        flash('Você não tem permissão para excluir este evento.', 'error')
        return redirect(url_for('meus_eventos'))
    
    try:
        db.session.delete(evento)
        db.session.commit()
        flash('Evento excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir evento.', 'error')
        print(f"Erro: {e}")
    
    return redirect(url_for('meus_eventos'))

@app.route('/eventos')
def listar_eventos():
    categoria = request.args.get('categoria')
    search = request.args.get('search')
    
    query = Evento.query
    
    if categoria and categoria != 'todos':
        query = query.filter_by(categoria=categoria)
    
    if search:
        query = query.filter(Evento.titulo.ilike(f'%{search}%'))
    
    eventos = query.filter(Evento.data >= datetime.now().date()).order_by(Evento.data.asc()).all()
    
    categorias = [
        ('todos', 'Todos'),
        ('festas', 'Festas'),
        ('shows', 'Shows'),
        ('esportes', 'Esportes'),
        ('tecnologia', 'Tecnologia'),
        ('academico', 'Acadêmico'),
        ('cultural', 'Cultural'),
        ('workshop', 'Workshop'),
        ('outros', 'Outros')
    ]
    
    return render_template("eventos.html", eventos=eventos, categorias=categorias, categoria_selecionada=categoria)

@app.route('/dashboard-organizador')
@login_required
def dashboard_organizador():
    if session.get('user_type') != 'organizador':
        flash('Acesso não autorizado.', 'error')
        return redirect(url_for('inicio'))
    
    organizador_id = session['user_id']
    
    # Estatísticas básicas
    total_eventos = Evento.query.filter_by(Organizador_ID=organizador_id).count()
    eventos_futuros = Evento.query.filter(
        Evento.Organizador_ID == organizador_id,
        Evento.data >= datetime.now().date()
    ).count()
    
    # Próximos eventos
    proximos_eventos = Evento.query.filter(
        Evento.Organizador_ID == organizador_id,
        Evento.data >= datetime.now().date()
    ).order_by(Evento.data.asc()).limit(5).all()
    
    return render_template("dashboard_organizador.html", 
                         total_eventos=total_eventos,
                         eventos_futuros=eventos_futuros,
                         proximos_eventos=proximos_eventos)

#CRIAÇÃO DAS ROTAS DE INSCRIÇÃO EM EVENTOS

@app.route('/evento/<int:evento_id>')
def detalhes_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)
    ja_inscrito = False
    
    if g.user and session.get('user_type') == 'usuario':
        inscricao = Inscricao.query.filter_by(
            Usuario_ID=session['user_id'], 
            Evento_ID=evento_id
        ).first()
        ja_inscrito = inscricao is not None
    
    return render_template("detalhes_evento.html", 
                         evento=evento, 
                         ja_inscrito=ja_inscrito)

@app.route('/inscrever/<int:evento_id>', methods=['POST'])
@login_required
def inscrever_evento(evento_id):
    if session.get('user_type') != 'usuario':
        flash('Apenas usuários podem se inscrever em eventos.', 'error')
        return redirect(url_for('detalhes_evento', evento_id=evento_id))
    
    evento = Evento.query.get_or_404(evento_id)
    
    # Verificar se já está inscrito
    inscricao_existente = Inscricao.query.filter_by(
        Usuario_ID=session['user_id'],
        Evento_ID=evento_id
    ).first()
    
    if inscricao_existente:
        flash('Você já está inscrito neste evento.', 'warning')
        return redirect(url_for('detalhes_evento', evento_id=evento_id))
    
    try:
        nova_inscricao = Inscricao(
            Usuario_ID=session['user_id'],
            Evento_ID=evento_id
        )
        
        db.session.add(nova_inscricao)
        db.session.commit()
        
        flash(f'Inscrição no evento "{evento.titulo}" realizada com sucesso!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('Erro ao realizar inscrição. Tente novamente.', 'error')
        print(f"Erro: {e}")
    
    return redirect(url_for('detalhes_evento', evento_id=evento_id))

@app.route('/cancelar-inscricao/<int:evento_id>', methods=['POST'])
@login_required
def cancelar_inscricao(evento_id):
    if session.get('user_type') != 'usuario':
        flash('Apenas usuários podem cancelar inscrições.', 'error')
        return redirect(url_for('detalhes_evento', evento_id=evento_id))
    
    inscricao = Inscricao.query.filter_by(
        Usuario_ID=session['user_id'],
        Evento_ID=evento_id
    ).first_or_404()
    
    try:
        db.session.delete(inscricao)
        db.session.commit()
        flash('Inscrição cancelada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao cancelar inscrição.', 'error')
        print(f"Erro: {e}")
    
    return redirect(url_for('detalhes_evento', evento_id=evento_id))

@app.route('/minhas-inscricoes')
@login_required
def minhas_inscricoes():
    if session.get('user_type') != 'usuario':
        flash('Apenas usuários podem ver suas inscrições.', 'error')
        return redirect(url_for('inicio'))
    
    inscricoes = Inscricao.query.filter_by(
        Usuario_ID=session['user_id']
    ).order_by(Inscricao.data_inscricao.desc()).all()
    
    return render_template("minhas_inscricoes.html", inscricoes=inscricoes)

#CRIA ROTA DA API PARA BUSCAR EVENTOS

@app.route('/api/eventos')
def api_eventos():
    
    try:
        # Buscar eventos futuros, ordenados por data
        eventos = Evento.query.filter(
            Evento.data >= datetime.now().date()
        ).order_by(Evento.data.asc()).limit(12).all()
        
        eventos_data = []
        for evento in eventos:
            eventos_data.append({
                'id': evento.ID,
                'titulo': evento.titulo,
                'descricao': evento.descricao,
                'local': evento.local,
                'data': evento.data.strftime('%d/%m/%Y'),
                'horario': evento.horario.strftime('%H:%M'),
                'categoria': evento.categoria,
                'imagem_url': evento.imagem_url or '/static/assets/img/default-event.jpg',
                'organizador': evento.organizador.nome if evento.organizador else 'Organizador'
            })
        
        return jsonify({
            'success': True,
            'eventos': eventos_data,
            'total': len(eventos_data)
        })
        
    except Exception as e:
        print(f"Erro ao buscar eventos: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro ao carregar eventos',
            'eventos': []
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5152)