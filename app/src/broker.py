from fastapi import FastAPI, Request
import threading
import requests
import asyncio

app = FastAPI()
queue = asyncio.Queue()

API_URL = "http://127.0.0.1:8001" #broker no 8k e server no 8k01
# mapeia rotas de client->broker para broker->server
#mesmo nome soh pq sim, da pra mudar pra ficar melhor (?eu acho?)
URL_MAP = {
    "reservas": "reservas",
    "locais": "locais",
}

class Event:
    def __init__(self, target, method, data):
        self.target = f"{API_URL}/{URL_MAP[target]}"
        self.method = method
        self.data = data
        self.result = "Erro Genérico"
        self.msg = "Erro Genérico Não Tratado"
        self.done = asyncio.Event()

#-------- fica como exercicio para o leitor ---------#

#balanceia carga entre diversas api's destino (soh precisa mudar o target url)
#podendo levar em consideracao o tipo de evento, tamanho da fila ou sla oq
#se algm quiser fazer ax q soh mete um id na url resolve 'API_URL/API_ID/<resto>'
#--n planejo fazer isso agr e talvez nem dps teria q testar e tudo, parece chato
def loadBalancing(current_event, event_queue):
    return; #nao fazer nada => n muda o destino => serve apenas pra servidor unico

#----------------------------------------------------#

@app.api_route("/{target}", methods=["GET", "POST"])
async def newEvent(target, request:Request):
    data = None if request.method == "GET" else await request.json()
    
    #adiciona novo evento a fila
    event = Event(URL_MAP[target], request.method, data)
    await queue.put(event)

    #espera evento ser processado
    await event.done.wait()

    #retorna resultados
    return {"status": event.result, "msg": event.msg, "data": event.data}

async def process_events():
    while True:
        event = await queue.get()

        #atualiza url target para balancear a carga entre destinos
        loadBalancing(event, queue)

        if event.method == "GET":
            r = requests.get(event.target).json()
            event.data = r['data']
        elif event.method == "POST":
            r = requests.post(event.target, json=event.data).json()
        else:
            r = {'status':'erro', 'msg':'nem get nem post (?)', 'data': -666}
        ###
        ###
        #supoe q r.json() deu boa, pode dar erro se n tiver nd pra jsonificar
        ###
        ###
        event.result = r['status']
        event.msg = r['msg']

        event.done.set()
        queue.task_done()

loop = asyncio.get_event_loop()
loop.create_task(process_events())
