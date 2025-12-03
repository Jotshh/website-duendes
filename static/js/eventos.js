class EventosManager {
    constructor() {
        this.eventos = [];
        this.init();
    }

    init() {
        this.carregarEventos();
        this.setupEventListeners();
    }

    async carregarEventos() {
        try {
            this.mostrarLoading();
            
            const response = await fetch('/api/eventos');
            const data = await response.json();
            
            if (data.success) {
                this.eventos = data.eventos;
                this.renderizarEventos();
            } else {
                this.mostrarErro('Erro ao carregar eventos');
            }
        } catch (error) {
            console.error('Erro:', error);
            this.mostrarErro('Erro de conexão');
        }
    }

    renderizarEventos() {
        const container = document.getElementById('eventos-dinamicos');
        if (!container) return;

        if (this.eventos.length === 0) {
            container.innerHTML = this.getHTMLSemEventos();
            return;
        }

        container.innerHTML = this.eventos.map(evento => this.getHTMLCardEvento(evento)).join('');
    }

    getHTMLCardEvento(evento) {
        return `
            <div class="event-card">
                <img src="${evento.imagem_url}" alt="${evento.titulo}" 
                     onerror="this.src='/static/assets/img/default-event.jpg'">
                <div class="card-content">
                    <h3>
                        <a href="/evento/${evento.id}">${evento.titulo}</a>
                    </h3>
                    <p>📅 ${evento.data} • ${evento.horario}</p>
                    <p>📍 ${evento.local}</p>
                    <p class="organizador-info">Por: ${evento.organizador}</p>
                    <span class="event-category">${this.formatarCategoria(evento.categoria)}</span>
                </div>
            </div>
        `;
    }

    getHTMLSemEventos() {
        return `
            <div class="empty-state">
                <div style="font-size: 4em; margin-bottom: 20px;">📅</div>
                <h3>Nenhum evento disponível</h3>
                <p>Não há eventos cadastrados no momento.</p>
                ${this.shouldShowCreateButton() ? 
                    '<a href="/criar-evento" class="btn-criar" style="margin-top: 15px;">Criar Primeiro Evento</a>' : 
                    '<a href="/eventos" class="btn-criar" style="margin-top: 15px;">Ver Todos os Eventos</a>'
                }
            </div>
        `;
    }

    formatarCategoria(categoria) {
        const categorias = {
            'festas': 'Festa',
            'shows': 'Show',
            'esportes': 'Esporte',
            'tecnologia': 'Tecnologia',
            'academico': 'Acadêmico',
            'cultural': 'Cultural',
            'workshop': 'Workshop',
            'outros': 'Outro'
        };
        return categorias[categoria] || categoria;
    }

    shouldShowCreateButton() {
        
        return document.body.innerHTML.includes('user_type') && 
               document.body.innerHTML.includes('organizador');
    }

    mostrarLoading() {
        const container = document.getElementById('eventos-dinamicos');
        if (container) {
            container.innerHTML = `
                <div class="loading-state">
                    <div class="loading-spinner"></div>
                    <p>Carregando eventos...</p>
                </div>
            `;
        }
    }

    mostrarErro(mensagem) {
        const container = document.getElementById('eventos-dinamicos');
        if (container) {
            container.innerHTML = `
                <div class="error-state">
                    <div style="font-size: 3em; margin-bottom: 15px;">❌</div>
                    <h3>Erro ao carregar</h3>
                    <p>${mensagem}</p>
                    <button onclick="eventosManager.carregarEventos()" class="btn-criar" style="margin-top: 15px;">
                        Tentar Novamente
                    </button>
                </div>
            `;
        }
    }

    setupEventListeners() {
        // Atualizar eventos a cada 5 minutos
        setInterval(() => {
            this.carregarEventos();
        }, 300000);
    }
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    window.eventosManager = new EventosManager();
});