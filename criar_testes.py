from app import app, db, Usuario, Organizador
from models import Organizador, Evento, Atividades
from datetime import datetime, timedelta


with app.app_context():
    try:
        print("🧪 Criando usuários de teste...")
        
        # Verificar se já existem usuários
        if Usuario.query.count() == 0:
            # Criar usuário de teste
            usuario_teste = Usuario(
                nome="João Silva",
                nome_usuario="joaosilva",
                CPF="123.456.789-00",
                email="joao@teste.com",
                telefone="(11) 99999-9999",
                tipo_usuario="participante"
            )
            usuario_teste.set_senha("123456")
            
            db.session.add(usuario_teste)
            db.session.commit()
            print("✅ Usuário de teste criado:")
            print("   Usuário: joaosilva")
            print("   Senha: 123456")
        
        print("🎉 Testes criados com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao criar testes: {e}")

with app.app_context():
    try:
        print("🧪 Criando organizador de teste...")
        
        # Verificar se já existe organizador
        if Organizador.query.filter_by(email="organizador@teste.com").first() is None:
            # Criar organizador de teste
            organizador_teste = Organizador(
                nome="Organizador Teste",
                email="organizador@teste.com",
                cpf_cnpj="00.000.000/0001-00",
                telefone="(11) 99999-9999"
            )
            organizador_teste.set_senha("123456")
            
            db.session.add(organizador_teste)
            db.session.commit()
            print("✅ Organizador de teste criado:")
            print("   Email: organizador@teste.com")
            print("   Senha: 123456")
        else:
            print("✅ Organizador de teste já existe")
        
    except Exception as e:
        print(f"❌ Erro ao criar organizador de teste: {e}")

with app.app_context():
    try:
        # Verificar se existe um organizador
        organizador = Organizador.query.first()
        if not organizador:
            print("❌ Nenhum organizador encontrado. Crie um organizador primeiro.")
        else:
            # Verificar se já existem eventos
            if Evento.query.count() == 0:
                # Criar eventos de teste
                eventos_teste = [
                    {
                        'titulo': 'Festa de Halloween',
                        'descricao': 'Venha com sua fantasia mais assustadora!',
                        'local': 'Clube Central',
                        'data': datetime.now().date() + timedelta(days=10),
                        'horario': datetime.strptime('20:00', '%H:%M').time(),
                        'categoria': 'festas',
                        'imagem_url': '/static/assets/img/embrasaween.jpg'
                    },
                    {
                        'titulo': 'Workshop de Programação Python',
                        'descricao': 'Aprenda Python do zero ao avançado',
                        'local': 'UFGD - Laboratório 5',
                        'data': datetime.now().date() + timedelta(days=5),
                        'horario': datetime.strptime('14:00', '%H:%M').time(),
                        'categoria': 'tecnologia',
                        'imagem_url': '/static/assets/img/workshop-python.jpg'
                    },
                    {
                        'titulo': 'Show de Rock Nacional',
                        'descricao': 'As melhores bandas de rock da região',
                        'local': 'Arena Music',
                        'data': datetime.now().date() + timedelta(days=20),
                        'horario': datetime.strptime('19:00', '%H:%M').time(),
                        'categoria': 'shows',
                        'imagem_url': '/static/assets/img/show-rock-nacional.webp'
                    },
                    {
                        'titulo': 'FESTIVAL DE VERÃO DE SALVADOR 2026',
                        'descricao': 'O Festival de Verão Salvador chega à sua 25ª edição, '
                        'reafirmando seu papel como um dos eventos musicais mais importantes e '
                        'longevos do Brasil. Mais do que um palco de shows, '
                        'o festival é um espaço de encontros e de celebração da diversidade cultural que marca a música brasileira. ',
                        'local': 'Arena Festival - Av. Luís Viana Filho,9581, Salvador - Bahia',
                        'data': datetime.now().date() + timedelta(days=25),
                        'horario': datetime.strptime('15:00', '%H:%M').time(),
                        'categoria': 'shows',
                        'imagem_url': '/static/assets/img/festival-verao.webp'
                    },
                    {
                        'titulo': 'Maratona de Programação',
                        'descricao': 'Com o objetivo de promover nos alunos a criatividade, '
                        'a capacidade de trabalho em equipe, a busca de novas soluções de software, '
                        'além da habilidade de resolver problemas sob pressão.',
                        'local': 'Centro Universitário IESB',
                        'data': datetime.now().date() + timedelta(days=15),
                        'horario': datetime.strptime('20:00', '%H:%M').time(),
                        'categoria': 'tecnologia',
                        'imagem_url': '/static/assets/img/maratona-programacao.png'
                    }
                ]
                
                for evento_data in eventos_teste:
                    evento = Evento(
                        titulo=evento_data['titulo'],
                        descricao=evento_data['descricao'],
                        local=evento_data['local'],
                        data=evento_data['data'],
                        horario=evento_data['horario'],
                        categoria=evento_data['categoria'],
                        Organizador_ID=organizador.ID,
                        imagem_url=evento_data['imagem_url']
                    )
                    db.session.add(evento)
                
                db.session.commit()
                print("✅ Eventos de teste criados com sucesso!")
            else:
                print("✅ Eventos já existem no banco")
                
    except Exception as e:
        print(f"❌ Erro ao criar eventos: {e}")

with app.app_context():
    try:
        print("🧪 Criando atividades de teste...")
        
        # Buscar eventos existentes
        eventos = Evento.query.all()
        
        if eventos and Atividades.query.count() == 0:
            atividades_teste = [
                {
                    'titulo': 'Palestra de Abertura',
                    'descricao': 'Palestra inicial sobre o tema do evento',
                    'data': eventos[0].data,
                    'horario_inicio': datetime.strptime('09:00', '%H:%M').time(),
                    'horario_fim': datetime.strptime('10:30', '%H:%M').time(),
                    'convidado': 'Dr. João Silva'
                },
                {
                    'titulo': 'Workshop Prático',
                    'descricao': 'Workshop hands-on para os participantes',
                    'data': eventos[0].data,
                    'horario_inicio': datetime.strptime('14:00', '%H:%M').time(),
                    'horario_fim': datetime.strptime('17:00', '%H:%M').time(),
                    'convidado': 'Prof. Maria Santos'
                }
            ]
            
            for atividade_data in atividades_teste:
                atividade = Atividades(
                    titulo=atividade_data['titulo'],
                    descricao=atividade_data['descricao'],
                    data=atividade_data['data'],
                    horario_inicio=atividade_data['horario_inicio'],
                    horario_fim=atividade_data['horario_fim'],
                    convidado=atividade_data['convidado'],
                    Evento_ID=eventos[0].ID
                )
                db.session.add(atividade)
            
            db.session.commit()
            print("✅ Atividades de teste criadas com sucesso!")
        else:
            print("✅ Atividades já existem ou não há eventos")
            
    except Exception as e:
        print(f"❌ Erro ao criar atividades: {e}")