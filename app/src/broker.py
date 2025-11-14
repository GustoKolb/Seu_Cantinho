from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
import threading
import requests
import asyncio
import time

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

queue = asyncio.Queue()
API_URL = "http://127.0.0.1:8001" #url da api de processamento de eventos

# mapeia rotas de client->broker para broker->server
# nomes traduzidos apenas pra demonstrar remapeamento
URL_MAP = {
    "reservas": "bookings",
    "locais": "places",
    "usuarios": "users",
    "imagens": "images",
}

class Event:
    def __init__(self, target, request, data):
        prefix = target.split('/')[0]
        suffix = '/'.join(target.split('/')[1:]) if len(target.split('/'))>1 else ''
        suffix = '?'+request.url.query if request.url.query else suffix

        self.target = f"{API_URL}/{URL_MAP[prefix]}/{suffix}"
        self.method = request.method
        self.data = data
        self.status = "Erro Genérico"
        self.msg = "Erro Genérico Não Tratado"
        self.done = asyncio.Event()

#metodo generico pra organizar todos os eventos recebidos
@app.api_route("/{target:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def newEvent(target, request:Request):
    data = None if request.method == "GET" else await request.json()
    
    #adiciona novo evento a fila
    event = Event(target, request, data)
    await queue.put(event)

    #espera evento ser processado
    await event.done.wait()

    #retorna status
    return {"status": event.status, "msg": event.msg, "data": event.data}

#processa os eventos da fila enviando para API(s) de processamento
async def process_events():
    while True:
        event = await queue.get()
        r = {}
        try:
            match event.method:
                case "GET":
                    r = requests.get(event.target).json()
                    event.data = r.get("data")
                case "POST":
                    r = requests.post(event.target, json=event.data).json()
                case "PUT":
                    r = requests.put(event.target, json=event.data).json()
                case "DELETE":
                    r = requests.delete(event.target, json=event.data).json()
                case _:
                    r = {'status':'error', 'msg':'Request Must Be "POST/GET/PUT/DELETE"'}
                    event.data = None
        except:
            r = {'status':'error', 'msg':'JSON Parse Error'}
            event.data = None

        event.status = r['status']
        event.msg = r['msg']

        event.done.set()
        queue.task_done()

loop = asyncio.get_event_loop()
loop.create_task(process_events())
