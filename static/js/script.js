// Espera o conteúdo da página carregar
document.addEventListener('DOMContentLoaded', () => {
    // Carrega os dois sliders ao mesmo tempo
    loadUpcomingEvents();
    loadRecentEvents();
    // Você pode adicionar uma função para carregar o "All Event" (Grid) também
});

// 1. Função para carregar "UPCOMING EVENTS"
async function loadUpcomingEvents() {
    try {
        // 1. Chama a nova API
        const response = await fetch('http://127.0.0.1:5000/api/events/upcoming');
        const events = await response.json();

        const sliderWrapper = document.querySelector('#upcoming-slider .swiper-wrapper');
        sliderWrapper.innerHTML = ''; // Limpa o conteúdo estático

        // 2. Cria os slides com os dados do banco (novos nomes de campos)
        events.forEach(event => {
            const slide = document.createElement('div');
            slide.className = 'swiper-slide';
            
            // ATENÇÃO: Usando os campos do seu banco (titulo, data, imagem_url)
            slide.innerHTML = `
                <img src="${event.imagem_url}" alt="${event.titulo}">
                <div class="slide-content">
                    <h3>${event.titulo}</h3>
                    <p>${formatarData(event.data)}</p>
                </div>
            `;
            sliderWrapper.appendChild(slide);
        });

        // 3. Inicializa o Swiper DEPOIS de adicionar os slides
        new Swiper('#upcoming-slider', {
            slidesPerView: 3,
            spaceBetween: 30,
            loop: true,
            navigation: {
                nextEl: '.upcoming-button-next',
                prevEl: '.upcoming-button-prev',
            },
        });

    } catch (error) {
        console.error("Erro ao carregar 'Upcoming Events':", error);
    }
}

// 2. Função para carregar "RECENT EVENTS"
async function loadRecentEvents() {
    try {
        // 1. Chama a nova API
        const response = await fetch('http://127.0.0.1:5000/api/events/past');
        const events = await response.json();

        const sliderWrapper = document.querySelector('#recent-slider .swiper-wrapper');
        sliderWrapper.innerHTML = ''; // Limpa o conteúdo estático

        // 2. Cria os slides com os dados do banco
        events.forEach(event => {
            const slide = document.createElement('div');
            slide.className = 'swiper-slide';
            
            // Usando os campos (titulo, data, imagem_url)
            slide.innerHTML = `
                <img src="${event.imagem_url}" alt="${event.titulo}">
                <div class="slide-content">
                    <h3>${event.titulo}</h3>
                    <p>${formatarData(event.data)}</p>
                </div>
            `;
            sliderWrapper.appendChild(slide);
        });

        // 3. Inicializa o Swiper
        new Swiper('#recent-slider', {
            slidesPerView: 4,
            spaceBetween: 30,
            loop: true,
            navigation: {
                nextEl: '.recent-button-next',
                prevEl: '.recent-button-prev',
            },
        });

    } catch (error) {
        console.error("Erro ao carregar 'Recent Events':", error);
    }
}

/**
 * Função Bônus: Formata a data de 'YYYY-MM-DD' para 'DD/MM/YYYY'
 */
function formatarData(dataISO) {
    const [ano, mes, dia] = dataISO.split('-');
    return `${dia}/${mes}/${ano}`;
}