from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from queue import Queue
import threading
import time

app = FastAPI() # comunicacao REST
reservas = []  # 'banco de dados' 
event_queue = Queue()  # fila de eventos

app = FastAPI()
reservas = []
event_queue = Queue()
result_dict = {}  # 

class Reserva(BaseModel):
    cliente: str
    espaco: str
    data: str
    request_id: str  # identificador único do cliente

def process_events():
    while True:
        reserva = event_queue.get() # retira evento da fila

		#switch case dos tipos de evento
		#<fazer>

		#---esses eh do post reserva---
		#verifica se o espaco ja foi reservado
        exists = any(r.espaco == reserva.espaco and r.data == reserva.data for r in reservas)
        if exists:
            result_dict[reserva.request_id] = {"status": "erro", "msg": "Espaço já reservado"}
        else:
            reservas.append(reserva)
            result_dict[reserva.request_id] = {"status": "ok", "msg": "Reserva criada"}
        event_queue.task_done()

@app.post("/reservas")
def criar_reserva(reserva: Reserva):
	#adiciona tipo do evento POST/GET reserva/pessoa pra processamento posterior
	#<fazer>

    event_queue.put(reserva) #coloca na fila
    while reserva.request_id not in result_dict: # espera ser processado
        time.sleep(0.01)

    result = result_dict.pop(reserva.request_id) # pega resultado
    if result["status"] == "erro":
        raise HTTPException(status_code=400, detail=result["msg"])
    return result

@app.get("/reservas")
def get_reservas():
	return reservas

threading.Thread(target=process_events, daemon=True).start() # inicia thread que processa eventos
