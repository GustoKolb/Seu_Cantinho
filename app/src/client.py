import requests
import uuid

BASE = "http://127.0.0.1:8000"  # endereço do servidor

def criar_reserva(cliente, espaco, data):
    request_id = str(uuid.uuid4())
    payload = {
        "cliente": cliente,
        "espaco": espaco,
        "data": data,
        "request_id": request_id
    }
    r = requests.post(f"{BASE}/reservas", json=payload)
    if r.status_code == 200:
        print(f"[{cliente}] Sucesso: {r.json()}")
    else:
        print(f"[{cliente}] Erro {r.status_code}: {r.json()}")

def listar_reservas():
    r = requests.get(f"{BASE}/reservas")
    for res in r.json():
        print(res)

if __name__ == "__main__":
    # Simula 3 clientes tentando reservar o mesmo espaço/data
    criar_reserva("João", "Chácara 1", "2025-10-15")
    criar_reserva("Maria", "Chácara 1", "2025-10-15")
    criar_reserva("Ana", "Chácara 1", "2025-10-15")

    print("Reservas processadas:")
    listar_reservas()
