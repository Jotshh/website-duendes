from app import app, db, Usuario, Organizador
from models import Organizador, Evento
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
                        'imagem_url': '/static/assets/img/ufgd.webp'
                    },
                    {
                        'titulo': 'Show de Rock Nacional',
                        'descricao': 'As melhores bandas de rock da região',
                        'local': 'Arena Music',
                        'data': datetime.now().date() + timedelta(days=15),
                        'horario': datetime.strptime('19:00', '%H:%M').time(),
                        'categoria': 'shows',
                        'imagem_url': '/static/assets/img/project-x.jpg'
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