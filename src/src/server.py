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

ENDPOINT_PLACES = os.getenv("ENDPOINT_PLACES")
ENDPOINT_BOOKINGS = os.getenv("ENDPOINT_BOOKINGS")
ENDPOINT_USERS = os.getenv("ENDPOINT_USERS")
ENDPOINT_IMAGES = os.getenv("ENDPOINT_IMAGES")

# mapeamento de url target pra nome do objeto usado nas funcoes
def get_object_name(target):
    if target == ENDPOINT_PLACES:
        return 'place'
    if target == ENDPOINT_BOOKINGS:
        return 'booking'
    if target == ENDPOINT_USERS:
        return 'user'
    return None

# processar resultado
def process_exit_code(method, target, exit_code):
    ok = exit_code == 0
    match exit_code:
        case -1: msg = f"Endpoint Inexistente /{target}"
        case 0: msg = f"{method} /{target} executado com sucesso"
        case 1: msg = f"Parâmetro inválido em {method} /{target}"
        case 2: msg = f"Erro ao Ler Banco de Dados em {method} /{target}"
        case _: msg = f"Erro desconhecido ({exit_code}) em {method} /{target}"
    return {'ok': ok, 'msg': msg}

# ----------------------------------------------------------------------

# por simplicidade, para não precisar usar tokens e controles de sessão/verificação
# POST especifico pra login de usuarios, se for login válido, retorna proprio user
@app.post('/login')
async def handle_login(request:Request):
    data = await request.json()
    if data['user'] is None or data['password'] is None:
        return process_exit_code('POST', '/login', 1)

    #pesquisa usuarios que tem nome e senha correspondentes aos parametros
    user = dbManager.read_user(byName=data['user'], byPassword=data['password'])
    if type(user) == list:
        user = user[0] if len(user)>0 else None

    if user is None:
        return process_exit_code('POST', '/login', 1)
    
    r = process_exit_code('POST', '/login', 0)
    r['data'] = user.isAdmin
    return r

@app.post("/{target}")
async def handle_post(target, request:Request):
    data = await request.json()
   
    obj = get_object_name(target)
    exit_code = -1
    if obj:
        func = getattr(dbManager, f"create_{obj}", None)
        exit_code = func(**data)
   
    return process_exit_code("POST", target, exit_code)

# ----------------------------------------------------------------------

@app.patch("/{target}/{t_id}")
async def handle_patch(target, t_id, request:Request):
    data = await request.json()
    
    obj = get_object_name(target)
    exit_code = -1
    if obj:
        func = getattr(dbManager, f"update_{obj}", None)
        data['id'] = t_id 
        exit_code = func(**data)
    
    return process_exit_code("PATCH", target, exit_code)

# ----------------------------------------------------------------------

@app.delete("/{target}/{t_id}")
async def handle_delete(target, t_id):
    obj = get_object_name(target)
    exit_code = -1
    if obj:
        func = getattr(dbManager, f"delete_{obj}", None)
        exit_code = func(id=t_id)
    
    return process_exit_code("DELETE", target, exit_code)

# ----------------------------------------------------------------------

#GET especifico pra carregamento de imagens
@app.get(f"/{ENDPOINT_IMAGES}/{{filename}}")
def get_file(filename):
    path = os.path.join(IMAGE_FOLDER, filename)

    b64 = None
    exit_code = -1 
    if os.path.isfile(path):
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            exit_code = 0

    r = process_exit_code("GET", f"/{ENDPOINT_IMAGES}/{{filename}}", exit_code)
    r["data"] = b64
    return r

#GET generico pra acesso ao bd
@app.get("/{target}")
def get_target(target: str, request: Request):
    filters = dict(request.query_params)

    obj = get_object_name(target)
    results = None
    exit_code = -1
    if obj:
        try:
            func = getattr(dbManager, f"read_{obj}", None)
            results = func(**filters)
            exit_code = 0
        except:
            exit_code = 2

    r = process_exit_code("GET", target, exit_code)
    r['data'] = results
    return r
