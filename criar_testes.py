from app import app, db, Usuario, Organizador
from app import app, db, Organizador

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