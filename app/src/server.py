from fastapi import FastAPI, Request

app = FastAPI() # comunicacao REST
reservas = [] # bd

@app.post("/reservas")
async def criar_reserva(request: Request):
    reservas.append(await request.json())
    return {'status':'ok', 'msg':'Nova Reserva Criada'}

@app.get("/reservas")
def get_reservas():
    return {'status':'ok','msg':'Todas as Reservas Retornadas','data':reservas}
