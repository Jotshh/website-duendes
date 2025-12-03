    document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const tipoToggle = document.getElementById('tipoToggle');
    const tipoInput = document.getElementById('tipoInput');
    const camposUsuario = document.getElementById('camposUsuario');
    const camposOrganizador = document.getElementById('camposOrganizador');
    const senhaInput = document.getElementById('senha');
    const confirmaSenhaInput = document.getElementById('confirma_senha');
    const strengthBar = document.querySelector('.strength-bar');
    const strengthText = document.querySelector('.strength-text');
    const form = document.getElementById('cadastroForm');
    const submitBtn = document.getElementById('submitBtn');
    
    // Alternar entre usuário e organizador
    tipoToggle.addEventListener('click', function(e) {
        if (e.target.classList.contains('tipo-option')) {
            // Remover classe active de todos
            document.querySelectorAll('.tipo-option').forEach(opt => {
                opt.classList.remove('active');
            });
            
            // Adicionar classe active ao clicado
            e.target.classList.add('active');
            
            // Atualizar campo hidden
            const tipo = e.target.getAttribute('data-type');
            tipoInput.value = tipo;
            
            // Mostrar/esconder campos específicos
            if (tipo === 'usuario') {
                camposUsuario.style.display = 'block';
                camposOrganizador.style.display = 'none';
            } else {
                camposUsuario.style.display = 'none';
                camposOrganizador.style.display = 'block';
            }
        }
    });
    
    // Verificar força da senha
    senhaInput.addEventListener('input', function() {
        const senha = this.value;
        let strength = 0;
        let text = '';
        
        // Verificar comprimento
        if (senha.length >= 8) strength++;
        
        // Verificar se tem números
        if (/\d/.test(senha)) strength++;
        
        // Verificar se tem letras maiúsculas
        if (/[A-Z]/.test(senha)) strength++;
        
        // Verificar se tem caracteres especiais
        if (/[^A-Za-z0-9]/.test(senha)) strength++;
        
        // Atualizar barra e texto
        const width = (strength / 4) * 100;
        strengthBar.style.width = width + '%';
        
        switch(strength) {
            case 0:
                text = 'Muito fraca';
                strengthBar.style.backgroundColor = '#dc3545';
                break;
            case 1:
                text = 'Fraca';
                strengthBar.style.backgroundColor = '#ff6b6b';
                break;
            case 2:
                text = 'Razoável';
                strengthBar.style.backgroundColor = '#ffd166';
                break;
            case 3:
                text = 'Boa';
                strengthBar.style.backgroundColor = '#06d6a0';
                break;
            case 4:
                text = 'Excelente';
                strengthBar.style.backgroundColor = '#118ab2';
                break;
        }
        
        strengthText.textContent = text;
    });
    
    // Verificar se as senhas coincidem
    function verificarSenhas() {
        if (senhaInput.value !== confirmaSenhaInput.value) {
            confirmaSenhaInput.style.borderColor = '#dc3545';
            confirmaSenhaInput.style.boxShadow = '0 0 0 3px rgba(220, 53, 69, 0.1)';
            return false;
        } else {
            confirmaSenhaInput.style.borderColor = '#28a745';
            confirmaSenhaInput.style.boxShadow = '0 0 0 3px rgba(40, 167, 69, 0.1)';
            return true;
        }
    }
    
    senhaInput.addEventListener('input', verificarSenhas);
    confirmaSenhaInput.addEventListener('input', verificarSenhas);
    
    // Validação do formulário antes de enviar
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        // Validar se os campos específicos estão preenchidos
        const tipo = tipoInput.value;
        
        if (tipo === 'usuario') {
            const usuario = document.getElementById('usuario').value;
            const cpf = document.getElementById('cpf').value;
            
            if (!usuario.trim()) {
                alert('Por favor, preencha o nome de usuário');
                isValid = false;
            }
            
            if (!cpf.trim()) {
                alert('Por favor, preencha o CPF');
                isValid = false;
            }
        } else {
            const cpfCnpj = document.getElementById('cpf_cnpj').value;
            
            if (!cpfCnpj.trim()) {
                alert('Por favor, preencha o CPF/CNPJ');
                isValid = false;
            }
        }
        
        // Verificar se as senhas coincidem
        if (!verificarSenhas()) {
            alert('As senhas não coincidem!');
            isValid = false;
        }
        
        // Verificar termos de uso
        const termos = document.getElementById('termos');
        if (!termos.checked) {
            alert('Você precisa concordar com os Termos de Uso');
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault();
        } else {
            // Desabilitar botão para evitar múltiplos cliques
            submitBtn.disabled = true;
            submitBtn.textContent = 'Criando conta...';
        }
    });
});