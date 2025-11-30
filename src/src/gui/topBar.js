//carrega soh se tiver logado
(function() {
    const userIsAdmin = localStorage.getItem('userIsAdmin');
    if (!userIsAdmin){
        console.warn('Acesso negado. Redirecionando para a página de login.');
        window.location.href = 'login.html';
    }
})();

/* cria o dropdown global */
document.addEventListener("DOMContentLoaded", () => {
    // cria container
    const dd = document.createElement("div");
    dd.id = "dropdown-global";
    dd.style.position = "fixed";
    dd.style.top = "60px";
    dd.style.right = "0";
    dd.style.background = "#333";
    dd.style.padding = "10px";
    dd.style.border = "1px solid #ff6600";
    dd.style.width = "10rem";
    dd.style.display = "none";
    dd.style.zIndex = "99999";

    dd.innerHTML = ''
    if (localStorage.getItem('userIsAdmin') == 'true')//libera administracao pra admins
        dd.innerHTML += `<button onclick='window.location.href = "administracao.html"'>Administração</button>`;
    dd.innerHTML += `<button onclick='window.location.href = "login.html"'>Sair</button>`;

    const botoes = dd.querySelectorAll("button");
    botoes.forEach(btn => {
        btn.style.width = "100%";
        btn.style.padding = "8px";
        btn.style.background = "#444";
        btn.style.color = "white";
        btn.style.border = "none";
        btn.style.borderRadius = "4px";
        btn.style.cursor = "pointer";
        btn.style.marginTop = "8px";
    });

    // adiciona ao body
    document.body.appendChild(dd);
});

function triggerSearch(){
    if (window.parent && window.parent.onTopbarSearch)
        window.parent.onTopbarSearch(window.getFilters())
}

/* conecta o botão do avatar do iframe ao dropdown global */
window.addEventListener("DOMContentLoaded", () => {
    const frame = document.querySelector("iframe[src='topBar.html']");
    if (!frame) return;

    frame.onload = () => {
        const btnA = frame.contentWindow.document.getElementById("avatar-btn");
        if (!btnA) return;

        btnA.onclick = () => {
            const dd = document.getElementById("dropdown-global");
            dd.style.display = dd.style.display === "none" ? "block" : "none";
        };

        const btnF = frame.contentWindow.document.getElementById("filter-btn");
        if (!btnF) return;

        btnF.onclick = () => {
            setFiltersPosition();
            const dd = document.getElementById("filters-dropdown-global");
            dd.style.display = dd.style.display === "none" ? "block" : "none";
        };

        frame.contentWindow.document.getElementById("search-btn").onclick = triggerSearch;
        frame.contentWindow.document.getElementById("search-input").addEventListener("keydown", (e) => {
            if (e.key === "Enter") triggerSearch();
        });

    };
});


//funcoes de pesquisa com filtros opcionais
window.fetchPlaces = async function(filters={}){
    const frame = document.querySelector("iframe[src='topBar.html']");
    if (!frame) return [];
    const BROKER_URL = window.CONFIG.BROKER_URL;
    const ENDPOINT_LOCAIS = window.CONFIG.ENDPOINT_LOCAIS;

    // monta query string a partir do objeto filters
    let query = new URLSearchParams();

    for (const key in filters) {
        if (filters[key] !== undefined && filters[key] !== null) {
            query.append(key, filters[key]);
        }
    }

    if (typeof(filters) == typeof(''))
        query=filters
            
    const locais = await fetch(`${BROKER_URL}/${ENDPOINT_LOCAIS}/?${query.toString()}`).then(j => j.json()).then(d=>d.data)
    locais.sort((a, b) => a.id - b.id);
    return locais
};

//filtros
window.getFilters = ()=>{
    const frame = document.querySelector("iframe[src='topBar.html']");
    let searchString = '';
    if (frame)
        searchString = frame.contentWindow.document.getElementById('search-input').value.trim()
    else
        searchString = document.getElementById('search-input').value.trim()
    
    const filters = {
        byName:     searchString,
        byCountry:  document.getElementById('filter-country').value.trim(),
        byState:    document.getElementById('filter-state').value.trim(),
        byCity:     document.getElementById('filter-city').value.trim(),
        district:   document.getElementById('filter-district').value.trim(),
        byPriceMin: document.getElementById('filter-price-min').value,
        byPriceMax: document.getElementById('filter-price-max').value,
        byCapacityMin: document.getElementById('filter-capacity-min').value,
        byCapacityMax: document.getElementById('filter-capacity-max').value,
    };
    
    // Remove campos vazios ou null/undefined
    Object.keys(filters).forEach(key => {
        if (filters[key] === "" || filters[key] == null) {
            delete filters[key];
        }
    });

    return filters;
}

window.addEventListener("DOMContentLoaded", () => {
    // cria dropdown global
    const filterDropdown = document.createElement("div");
    filterDropdown.id = "filters-dropdown-global";
    filterDropdown.style.position = "fixed";
    filterDropdown.style.top = "60px"; // abaixo da topbar
    filterDropdown.style.background = "#333";
    filterDropdown.style.padding = "10px";
    filterDropdown.style.borderRadius = "5px";
    filterDropdown.style.border = "1px solid #ff6600";
    filterDropdown.style.display = "none";
    filterDropdown.style.zIndex = "9999";

    const defStyle = 'style="display:block; margin-bottom:5px;"';
    filterDropdown.innerHTML = `
        <input placeholder="País" id="filter-country" ${defStyle}>
        <input placeholder="Estado" id="filter-state" ${defStyle}>
        <input placeholder="Cidade" id="filter-city" ${defStyle}>
        <input placeholder="Bairro" id="filter-district" ${defStyle}>
        <input placeholder="Preço Mínimo" type="number" id="filter-price-min" ${defStyle}>
        <input placeholder="Preço Máximo" type="number" id="filter-price-max" ${defStyle}>
        <input placeholder="Capacidade Mínima" type="number" id="filter-capacity-min"  ${defStyle}>
        <input placeholder="Capacidade Máxima" type="number" id="filter-capacity-max"  ${defStyle}>
    `;
    document.body.appendChild(filterDropdown);

    // enter em qualquer input do dropdown também dispara
    filterDropdown.querySelectorAll("input").forEach(input => {
        input.addEventListener("keydown", e => {
            if (e.key === "Enter" && window.parent && window.parent.onTopbarSearch)
                window.parent.onTopbarSearch(window.getFilters());
        });
    });
});

function setFiltersPosition(){
    const frame = document.querySelector("iframe[src='topBar.html']");
    const dropdown = document.getElementById("filters-dropdown-global");

    const btn = frame.contentWindow.document.getElementById("filter-btn");
    if (!btn) return;

    const rect = btn.getBoundingClientRect();
    const left = rect.left + window.scrollX;

    dropdown.style.position = "absolute";
    dropdown.style.left = `${left}px`;
}

