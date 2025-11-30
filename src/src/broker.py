from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
import threading
import requests
import asyncio
import time
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

queue = asyncio.Queue()

#env definido via docker
API_URL = os.getenv("SERVER_URL")
# mapeia rotas de client->broker para broker->server
# nomes traduzidos apenas pra demonstrar remapeamento
URL_MAP = {
    os.getenv("ENDPOINT_RESERVAS") : os.getenv("ENDPOINT_BOOKINGS"),
    os.getenv("ENDPOINT_LOCAIS")   : os.getenv("ENDPOINT_PLACES"),
    os.getenv("ENDPOINT_USUARIOS") : os.getenv("ENDPOINT_USERS"),
    os.getenv("ENDPOINT_IMAGENS")  : os.getenv("ENDPOINT_IMAGES"),
    os.getenv("ENDPOINT_LOGIN")    : os.getenv("ENDPOINT_LOGIN"),
}

class Event:
    def __init__(self, target, request, data):
        prefix = target.split('/')[0]
        suffix = '/'.join(target.split('/')[1:]) if len(target.split('/'))>1 else ''
        suffix = '?'+request.url.query if request.url.query else suffix

        self.target = f"{API_URL}/{URL_MAP[prefix]}/{suffix}"
        self.method = request.method
        self.data = data
        self.response = {"ok":False, 'msg':'New Event', 'data':None}
        self.done = asyncio.Event()

#metodo generico pra organizar todos os eventos recebidos
@app.api_route("/{target:path}", methods=["GET", "POST", "PATCH", "DELETE"])
async def newEvent(target, request:Request):
    data = None
    if request.method == "POST" or request.method == 'PATCH':
        data = await request.json()
    
    #adiciona novo evento a fila
    event = Event(target, request, data)
    await queue.put(event)
    await event.done.wait()
    return event.response

#processa os eventos da fila enviando para API(s) de processamento
async def process_events():
    while True:
        event = await queue.get()
        r = {}
        try:
            request = getattr(requests, event.method.lower())
            if event.method ==  "GET":
                r = request(event.target).json()
            else:
                r = request(event.target, json=event.data).json()
        except:
            r = {'ok':False, 'msg':'JSON Parse Error', 'data':None}

        event.response = r
        event.done.set()
        queue.task_done()

asyncio.create_task(process_events())
