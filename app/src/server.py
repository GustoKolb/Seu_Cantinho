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
    "PATCH": "update",
    "DELETE": "delete",
}

ENDPOINT_PLACES = os.getenv("ENDPOINT_PLACES")
ENDPOINT_BOOKINGS = os.getenv("ENDPOINT_BOOKINGS")
ENDPOINT_USERS = os.getenv("ENDPOINT_USERS")
ENDPOINT_IMAGES = os.getenv("ENDPOINT_IMAGES")

@app.api_route("/{target}", methods=["POST", "PATCH", "DELETE"])
async def nonGetHandler(target, request: Request):
    data = await request.json()

    #mapeamento de metodos->acoes
    action = ACTIONS.get(request.method)
    if not action:
        return {'status': 'error', 'msg': f'Método {request.method} não suportado'}
    
    obj = None
    if target == ENDPOINT_PLACES:
        obj = 'place'
    if target == ENDPOINT_BOOKINGS:
        obj = 'booking'
    if target == ENDPOINT_USERS:
        obj = 'user'

    func_name = f"{action}_{obj}"
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
@app.get(f"/{ENDPOINT_IMAGES}/{{filename}}")
def get_file(filename):
    path = os.path.join(IMAGE_FOLDER, filename)

    if not os.path.isfile(path):
        raise HTTPException(404)
    
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    
    return {"status": "ok", 'msg':'Imagem Retornada em Base 64',"data": b64}

#GET generico pra acesso ao bd
@app.get("/{target}")
def get_target(target: str, request: Request):
    filters = dict(request.query_params)
    results=None

    try:
        if target == ENDPOINT_BOOKINGS:
            results = dbManager.read_booking(**filters)
        elif target == ENDPOINT_USERS:
            results = dbManager.read_user(**filters)
        elif target == ENDPOINT_PLACES:
            results = dbManager.read_place(**filters)

        msg = "Pesquisa Realizada Com Sucesso"
        status='ok'
    except:
        results = None
        status = 'error'
        msg = "Erro ao Ler Banco de Dados"

    return {'status':status, 'msg':msg, 'data':results}
