from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from urllib.parse import unquote
import json
import os
import base64
import db as dbManager

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#caminho pro diretorio de imagens
IMAGE_FOLDER = 'db/images/'

#prefixo pra construcao de nome da funcao
ACTIONS = {
    "POST": "create",
    "PUT": "update",
    "DELETE": "delete",
}

@app.api_route("/{target}", methods=["POST", "PUT", "DELETE"])
async def nonGetHandler(target, request: Request):
    data = await request.json()

    #define o metodo
    action = ACTIONS.get(request.method)
    if not action:
        return {'status': 'error', 'msg': f'Método {request.method} não suportado'}

    #constroi nome da funcao: create_user, update_place, etc...
    func_name = f"{action}_{target[:-1]}"
    func = getattr(dbManager, func_name, None)
    if not func:
        return {'status': 'error', 'msg': f"Endpoint inexistente (/{target})"}

    #executa funcao e processa exit_code
    exit_code = func(**data)
    status = 'ok' if exit_code == 0 else 'error'
    match exit_code:
        case  0: msg = f"{request.method} /{target} executado com sucesso"
        case  1: msg = f"Parâmetro inválido em {request.method} /{target}"
        case _:  msg = f"Erro desconhecido ({exit_code}) em {request.method} /{target} ({func_name})"

    return {'status': status, 'msg': msg}

#GET especifico pra carregamento de imagens
@app.get("/images/{filename}")
def get_file(filename):
    path = os.path.join(IMAGE_FOLDER, filename)

    if not os.path.isfile(path):
        raise HTTPException(404)
    
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    
    return {"status": "ok", 'msg':'Imagem Retornada em Base 64',"data": b64}

#GET generico pra acesso ao bd
@app.get("/{target}")
def get_target(target, search_string=None, search_filters=None):
    results=None
    try:
        match target:
            case 'bookings':
                results = dbManager.read_booking(byName=search_string)
            case 'users':
                results = dbManager.read_user(byName=search_string)
            case 'places':
                results = dbManager.read_place(byName=search_string)

        #aplica filtros do tipo atributo:
        #   o objeto possui aquele campo e com o valor especificado
        if search_filters:
            search_filters = json.loads(unquote(search_filters))
            results = [r for r in results if all(getattr(r, k, None) == v
                                             for k, v in search_filters.items())]

        msg = "Pesquisa Realizada Com Sucesso"
        status='ok'
    except:
        results = None
        status = 'error'
        msg = "Erro ao Ler Banco de Dados"

    return {'status':status, 'msg':msg, 'data':results}
