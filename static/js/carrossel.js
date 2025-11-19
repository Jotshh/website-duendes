class CarrosselEventos {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.carrossel = this.container.querySelector('.carrossel');
        this.prevBtn = this.container.querySelector('.carrossel-btn.prev');
        this.nextBtn = this.container.querySelector('.carrossel-btn.next');
        
        this.init();
    }
    
    init() {
        this.prevBtn.addEventListener('click', () => this.scroll(-1));
        this.nextBtn.addEventListener('click', () => this.scroll(1));
        
        this.updateButtonVisibility();
        this.carrossel.addEventListener('scroll', () => this.updateButtonVisibility());
        
        this.carrossel.addEventListener('wheel', (e) => {
            if (e.deltaY !== 0) {
                e.preventDefault();
                this.carrossel.scrollLeft += e.deltaY;
            }
        });
    }
    
    scroll(direction) {
        const cards = this.carrossel.querySelectorAll('.event-card');
        if (cards.length === 0) return;
        
        const cardWidth = cards[0].offsetWidth + 25; 
        const scrollAmount = cardWidth * direction;
        
        this.carrossel.scrollBy({
            left: scrollAmount,
            behavior: 'smooth'
        });
    }
    
    updateButtonVisibility() {
        const scrollLeft = this.carrossel.scrollLeft;
        const scrollWidth = this.carrossel.scrollWidth;
        const clientWidth = this.carrossel.clientWidth;
        
        this.prevBtn.style.opacity = scrollLeft > 0 ? '1' : '0.5';
        this.nextBtn.style.opacity = scrollLeft < (scrollWidth - clientWidth - 10) ? '1' : '0.5';
    }
    
    async carregarEventos() {
        try {
            this.mostrarLoading();
            
            const response = await fetch('/api/eventos');
            const data = await response.json();
            
            if (data.success) {
                this.renderizarEventos(data.eventos);
            } else {
                this.mostrarErro('Erro ao carregar eventos');
            }
        } catch (error) {
            console.error('Erro:', error);
            this.mostrarErro('Erro de conexão');
        }
    }
    
    renderizarEventos(eventos) {
        if (eventos.length === 0) {
            this.carrossel.innerHTML = this.getHTMLSemEventos();
            return;
        }

        this.carrossel.innerHTML = eventos.map(evento => this.getHTMLCardEvento(evento)).join('');
        this.updateButtonVisibility();
    }
    
    getHTMLCardEvento(evento) {
        return `
            <div class="event-card">
                <img src="${evento.imagem_url}" alt="${evento.titulo}" 
                     onerror="this.src='/static/assets/img/default-event.jpg'">
                <div class="event-content">
                    <h3 class="event-title">
                        <a href="/evento/${evento.id}">${evento.titulo}</a>
                    </h3>
                    <p class="event-info">📅 ${evento.data}</p>
                    <p class="event-info">🕒 ${evento.horario}</p>
                    <p class="event-info">📍 ${evento.local}</p>
                    <span class="event-category">${this.formatarCategoria(evento.categoria)}</span>
                </div>
            </div>
        `;
    }
    
    getHTMLSemEventos() {
        return `
            <div class="empty-state">
                <div style="font-size: 3em; margin-bottom: 15px;">📅</div>
                <h3>Nenhum evento disponível</h3>
                <p>Não há eventos cadastrados no momento.</p>
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
    
    mostrarLoading() {
        this.carrossel.innerHTML = `
            <div class="loading-state">
                <div class="loading-spinner"></div>
                <p>Carregando eventos...</p>
            </div>
        `;
    }
    
    mostrarErro(mensagem) {
        this.carrossel.innerHTML = `
            <div class="error-state">
                <div style="font-size: 3em; margin-bottom: 15px;">❌</div>
                <h3>Erro ao carregar</h3>
                <p>${mensagem}</p>
                <button onclick="carrossel.carregarEventos()" class="btn-ver-todos" style="margin-top: 15px;">
                    Tentar Novamente
                </button>
            </div>
        `;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const carrossel = new CarrosselEventos('carrossel-eventos');
    carrossel.carregarEventos();
    
    setInterval(() => {
        carrossel.carregarEventos();
    }, 300000);
});