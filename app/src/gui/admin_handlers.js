// --- admin-handlers-forms.js ---

// As seguintes variáveis e funções de utilidade serão usadas pelas funções de CRUD.

/**
 * @param {string} e - Nome da entidade (ex: 'usuarios')
 * @returns {string} - Nome da classe em português (ex: 'Usuário')
 */
function getEntityClass(e){
    switch (e){
        case 'usuarios': return 'Usuário';
        case 'reservas': return 'Reserva';
        case 'locais': return 'Local';
        default: return 'Indefinido';
    }
}

// Mapeamento de Funções de Formulário e Submissão
const entityMap = {
    'usuarios': { getFormHTML: getUsuariosFormHTML, submit: submitUsuariosForm },
    'locais': { getFormHTML: getLocaisFormHTML, submit: submitLocaisForm },
    'reservas': { getFormHTML: getReservasFormHTML, submit: submitReservasForm },
};

// --- FUNÇÕES DE LÓGICA CRUD ---

// DELETE: Handler de exclusão (window.handleDelete precisa ser definida no HTML para funcionar)
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
            alert(`${getEntityClass(entity)} deletado com sucesso!`);
            // Nota: Quem chamar handleDelete (no HTML) deve chamar loadEntity(entity)
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

// POST/PATCH: Handler de Criação/Edição
async function handleDataSubmit(entity, id, data, method = 'POST') {
    const config = window.CONFIG;
    const endpointKey = 'ENDPOINT_' + entity.toUpperCase();
    const endpoint = config[endpointKey];
    const action = method === 'POST' ? 'Criar' : 'Editar';

    const url = id ? `${config.BROKER_URL}/${endpoint}/${id}` : `${config.BROKER_URL}/${endpoint}`;
    
    let bodyData;
    let headers = {};

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
        });

        if (response.ok) {
            alert(`${getEntityClass(entity)} ${action} com sucesso!`);
            return true;
        } else {
            let error = await response.json().catch(() => ({ message: response.statusText }));
            alert(`Erro ao ${action.toLowerCase()}: ${error.message || response.statusText}`);
            return false;
        }
    } catch (error) {
        alert(`Erro de comunicação com o servidor ao ${action.toLowerCase()}.`);
        return false;
    }
}


// --- FUNÇÕES DE FORMULÁRIO (RENDERIZAÇÃO HTML) ---
        
function getUsuariosFormHTML(item = {}) {
    return `
        <input type="hidden" name="id" value="${item.id || ''}">
        <div class="form-group"><label for="name">Nome:</label><input type="text" id="name" name="name" value="${item.name || ''}" required></div>
        <div class="form-group"><label for="password">Senha:</label><input type="password" id="password" name="password" value="" placeholder="${item.id ? 'Deixe vazio para manter a senha atual' : ''}" ${item.id ? '' : 'required'}></div>
        <div class="form-group"><label for="filial_id">ID da Filial:</label><input type="number" id="filial_id" name="filial_id" value="${item.filial_id || ''}" required min="1"></div>
        <div class="form-group">
            <label for="isAdmin">Admin:</label>
            <select id="isAdmin" name="isAdmin" required>
                <option value="false" ${item.isAdmin === false || item.isAdmin === 'false' ? 'selected' : ''}>Não</option>
                <option value="true" ${item.isAdmin === true || item.isAdmin === 'true' ? 'selected' : ''}>Sim</option>
            </select>
        </div>
    `;
}

function getLocaisFormHTML(item = {}) {
    const isEdit = !!item.id;
    return `
        <input type="hidden" name="id" value="${item.id || ''}">
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
            <label for="image_upload">Nova Imagem (POST/Criação):</label>
            <input type="file" id="image_upload" name="image_upload" accept="image/*" ${isEdit ? 'disabled' : ''}>
            ${isEdit ? `<p style="font-size:0.9em; color:#999;">A edição de imagem é feita via endpoint específico.</p>` : ''}
            <div id="image-preview-container"></div>
        </div>
    `;
}
        
function getReservasFormHTML(item = {}) {
    const formatDate = (dateString) => dateString ? dateString.split('T')[0] : '';
    return `
        <input type="hidden" name="id" value="${item.booking_id || ''}">
        <div class="form-group"><label for="client_name">Nome do Cliente:</label><input type="text" id="client_name" name="client_name" value="${item.client_name || ''}" required></div>
        <div class="form-group"><label for="client_email">Email:</label><input type="email" id="client_email" name="client_email" value="${item.client_email || ''}" required></div>
        <div class="form-group"><label for="client_phone">Telefone:</label><input type="text" id="client_phone" name="client_phone" value="${item.client_phone || ''}" required></div>
        <div class="form-group"><label for="place_id">ID do Local:</label><input type="number" id="place_id" name="place_id" value="${item.place ? item.place.id : ''}" required min="1"></div>
        <div class="form-group"><label for="total_amount">Valor Total:</label><input type="number" id="total_amount" name="total_amount" value="${item.total_amount || ''}" required min="0" step="0.01"></div>
        <div class="form-group"><label for="amount_paid">Valor Pago:</label><input type="number" id="amount_paid" name="amount_paid" value="${item.amount_paid || ''}" required min="0" step="0.01"></div>
        <div class="form-group"><label for="start_date">Data Início:</label><input type="date" id="start_date" name="start_date" value="${formatDate(item.start_date)}" required></div>
        <div class="form-group"><label for="end_date">Data Fim:</label><input type="date" id="end_date" name="end_date" value="${formatDate(item.end_date)}" required></div>
    `;
}

// --- FUNÇÕES DE SUBMISSÃO (POST/PATCH) ---

async function submitUsuariosForm(entity, form) {
    const id = form.id.value;
    const method = id ? 'PATCH' : 'POST';
    const data = {
        name: form.name.value,
        filial_id: parseInt(form.filial_id.value),
        isAdmin: form.isAdmin.value === 'true',
    };
    if (form.password.value) { data.password = form.password.value; }
    return handleDataSubmit(entity, id, data, method);
}

async function submitLocaisForm(entity, form) {
    const id = form.id.value;
    const method = id ? 'PATCH' : 'POST';
    const data = {
        name: form.name.value, street: form.street.value, number: form.number.value, district: form.district.value, 
        city: form.city.value, state: form.state.value, country: form.country.value, description: form.description.value, 
        price: parseFloat(form.price.value), capacity: parseInt(form.capacity.value)
    };

    if (method === 'POST' && form.image_upload.files.length > 0) {
        const formData = new FormData();
        formData.append('data', JSON.stringify(data)); 
        formData.append('image', form.image_upload.files[0]);
        return handleDataSubmit(entity, id, formData, method);
    }
    return handleDataSubmit(entity, id, data, method);
}

async function submitReservasForm(entity, form) {
    const id = form.id.value;
    const method = id ? 'PATCH' : 'POST';
    const data = {
        client_name: form.client_name.value, client_email: form.client_email.value, client_phone: form.client_phone.value,
        amount_paid: parseFloat(form.amount_paid.value), total_amount: parseFloat(form.total_amount.value),
        place: parseInt(form.place_id.value), 
        start_date: form.start_date.value, end_date: form.end_date.value,
    };
    return handleDataSubmit(entity, id, data, method);
}