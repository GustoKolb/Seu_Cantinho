// pra melhor exibicao na interface
function getEntityClass(e){
    switch (e){
        case 'usuarios': return 'Usuário';
        case 'reservas': return 'Reserva';
        case 'locais': return 'Local';
        default: return 'Entidade Indefinida';
    }
}

// facilitar acesso por mapeamento generico
const entityMap = {
    'usuarios': { getFormHTML: getUsuariosFormHTML, submit: submitUsuariosForm },
    'locais'  : { getFormHTML: getLocaisFormHTML,   submit: submitLocaisForm },
    'reservas': { getFormHTML: getReservasFormHTML, submit: submitReservasForm },
};

//handle DELETE

window.handleDelete = async function(entity, id) {
    const config = window.CONFIG;
    if (!config) {
        console.error("CONFIG não está definido.");
        return false;
    }
    
    if (!confirm(`Tem certeza que deseja DELETAR o ${getEntityClass(entity)} com ID ${id}?`)) {
        return false;
    }

    const endpointKey = 'ENDPOINT_' + entity.toUpperCase();
    const endpoint = config[endpointKey];
    
    try {
        const url = `${config.BROKER_URL}/${endpoint}/${id}`;
        const response = await fetch(url, { method: 'DELETE' });

        if (response.ok) {
            alert(`Deletar ${getEntityClass(entity)}: Sucesso!`);
            return true;
        } else {
            const error = await response.json().catch(() => ({ message: response.statusText }));
            alert(`Erro ao deletar: ${error.message}`);
            return false;
        }
    } catch (error) {
        alert('Erro de comunicação com o servidor ao deletar.');
        return false;
    }
}

// POST e PATCH

async function handleDataSubmit(entity, id, data, method = 'POST') {
    const config = window.CONFIG;
    const endpointKey = 'ENDPOINT_' + entity.toUpperCase();
    const endpoint = config[endpointKey];
    const action = method === 'POST' ? 'Criar' : 'Editar';    
    const url = method === 'PATCH' ? `${config.BROKER_URL}/${endpoint}/${id}` : `${config.BROKER_URL}/${endpoint}`;
    
    let bodyData;
    let headers = {};
1
    if (data instanceof FormData) {
        bodyData = data;
    } else {
        bodyData = JSON.stringify(data);
        headers['Content-Type'] = 'application/json';
    }
    try {
        const response = await fetch(url, {
            method: method,
            headers: headers,
            body: bodyData,
        }).then(j=>j.json());

        if (!response.ok){
            alert(`Erro ao ${action.toLowerCase()}: Período Já Reservado`);
            return false;
        }
        
        alert(`${action} ${getEntityClass(entity)}: Sucesso!`);
        return true;

    } catch (error) {
        alert(`Erro de comunicação com o servidor ao ${action}.`);
        return false;
    }
}

///////////////// get forms

function getUsuariosFormHTML(item = {}) {
    const isEditing = item.id != null && Number.isInteger(Number(item.id)) && Number(item.id) >= 0;

    return `
        <input type="hidden" name="id" value="${item.id != null ? item.id : ''}">
        <div class="form-group"><label for="name">Nome</label><input type="text" id="name" name="name" value="${item.name || ''}" required></div>
        <div class="form-group"><label for="password">Senha</label><input type="text" id="password" name="password" value="${isEditing ? item.password:''}" 'required'></div>
        <div class="form-group"><label for="filial_id">ID da Filial</label><input type="number" id="filial_id" name="filial_id" value="${item.filial_id != null ? item.filial_id : ''}" required min="0"></div>
        <div class="form-group">
            <label for="isAdmin">É Administrador?</label>
            <select id="isAdmin" name="isAdmin" required>
                <option value="false" ${item.isAdmin === false || item.isAdmin === 'false' ? 'selected' : ''}>Não</option>
                <option value="true" ${item.isAdmin === true || item.isAdmin === 'true' ? 'selected' : ''}>Sim</option>
            </select>
        </div>
    `;
}

function getLocaisFormHTML(item = {}){
    return `
        <input type="hidden" name="id" value="${item.id != null ? item.id : ''}">
        <div class="form-group"><label for="name">Nome:</label><input type="text" id="name" name="name" value="${item.name || ''}" required></div>
        <div class="form-group"><label for="street">Endereço:</label><input type="text" id="street" name="street" value="${item.street || ''}" required></div>
        <div class="form-group"><label for="number">Número:</label><input type="text" id="number" name="number" value="${item.number || ''}" required></div>
        <div class="form-group"><label for="district">Bairro:</label><input type="text" id="district" name="district" value="${item.district || ''}" required></div>
        <div class="form-group"><label for="city">Cidade:</label><input type="text" id="city" name="city" value="${item.city || ''}" required></div>
        <div class="form-group"><label for="state">Estado:</label><input type="text" id="state" name="state" value="${item.state || ''}" required></div>
        <div class="form-group"><label for="country">País:</label><input type="text" id="country" name="country" value="${item.country || ''}" required></div>
        <div class="form-group"><label for="description">Descrição:</label><textarea id="description" name="description" required>${item.description || ''}</textarea></div>
        <div class="form-group"><label for="price">Preço:</label><input type="number" id="price" name="price" value="${item.price || ''}" required min="0" step="0.01"></div>
        <div class="form-group"><label for="capacity">Capacidade:</label><input type="number" id="capacity" name="capacity" value="${item.capacity || ''}" required min="1"></div>
        <div class="form-group">
            <label for="image_upload">Imagem</label>
            <input type="file" id="image_upload" name="image_upload" accept="image/*">
            <div id="image-preview-container"></div>
        </div>
    `;
}

function getReservasFormHTML(item = {}){
    const toYMD = (dmy) => dmy.split('-').reverse().join('-'); //converte dmy pra ymd
    const placeIdValue = item.place ? (item.place.id != null ? item.place.id : '') : '';

    return `
        <input type="hidden" name="id" value="${item.id != null ? item.id : ''}">
        <div class="form-group"><label for="client_name">Nome do Cliente:</label><input type="text" id="client_name" name="client_name" value="${item.client_name || ''}" required></div>
        <div class="form-group"><label for="client_email">Email:</label><input type="email" id="client_email" name="client_email" value="${item.client_email || ''}" required></div>
        <div class="form-group"><label for="client_phone">Telefone:</label><input type="text" id="client_phone" name="client_phone" value="${item.client_phone || ''}" required></div>
        <div class="form-group"><label for="place_id">ID do Local:</label><input type="number" id="place_id" name="place_id" value="${placeIdValue}" required min="0"></div>
        <div class="form-group"><label for="total_amount">Valor Total:</label><input type="number" id="total_amount" name="total_amount" value="${item.total_amount || ''}" required min="0" step="0.01"></div>
        <div class="form-group"><label for="amount_paid">Valor Pago:</label><input type="number" id="amount_paid" name="amount_paid" value="${item.amount_paid || ''}" required min="0" step="0.01"></div>
        <div class="form-group"><label for="start_date">Data de Início:</label><input type="date" id="start_date" name="start_date" value="${toYMD(item.start_date)}" required></div>
        <div class="form-group"><label for="end_date">Data de Término:</label><input type="date" id="end_date" name="end_date" value="${toYMD(item.end_date)}" required></div>
    `;
}

////////////////// submit forms

async function submitUsuariosForm(entity, form){
    const rawId = form.id.value;
    const id = rawId !== '' ? parseInt(rawId) : null;
    const isEditing = Number.isInteger(id) && id >= 0;
    const method = isEditing ? 'PATCH' : 'POST';
    
    const data = {
        name: form.name.value,
        filial_id: parseInt(form.filial_id.value), 
        isAdmin: form.isAdmin.value === 'true',
    };
    
    if (form.password.value) { data.password = form.password.value; }
    return handleDataSubmit(entity, id, data, method);
}

function file2b64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
}

async function submitLocaisForm(entity, form) {
    const rawId = form.id.value;
    const id = rawId !== '' ? parseInt(rawId) : null;
    
    const isEditing = Number.isInteger(id) && id >= 0;
    const method = isEditing ? 'PATCH' : 'POST';
    
    const data = {
        name: form.name.value, street: form.street.value, number: form.number.value, district: form.district.value, 
        city: form.city.value, state: form.state.value, country: form.country.value, description: form.description.value, 
        price: parseFloat(form.price.value), capacity: parseInt(form.capacity.value)
    };

    if (form.image_upload.files.length > 0)
        data.image_b64 = await file2b64(form.image_upload.files[0]);

    return handleDataSubmit(entity, id, data, method);
}

async function submitReservasForm(entity, form){
    const rawId = form.id.value;
    const id = rawId !== '' ? parseInt(rawId) : null;
    const isEditing = Number.isInteger(id) && id >= 0;
    const method = isEditing ? 'PATCH' : 'POST';
    const toDMY = (ydm) => ydm.split('-').reverse().join('-');

    if (new Date(form.start_date.value) > new Date(form.end_date.value)){
        alert("Erro: Data de Início Maior que Término")
        return false;
    }

    const data = {
        client_name: form.client_name.value,
        client_email: form.client_email.value,
        client_phone: form.client_phone.value,
        amount_paid: parseFloat(form.amount_paid.value),
        total_amount: parseFloat(form.total_amount.value),
        place_id: parseInt(form.place_id.value), 
        start_date: toDMY(form.start_date.value),
        end_date: toDMY(form.end_date.value),
    };

    return handleDataSubmit(entity, id, data, method);
}