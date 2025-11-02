import requests

BROKER_IP = "http://127.0.0.1:8000"

ENDPOINTS = {
    "usuarios": f"{BROKER_IP}/usuarios",
    "locais": f"{BROKER_IP}/locais",
    "reservas": f"{BROKER_IP}/reservas",
}


def req(method, endpoint, payload=None):
    url = ENDPOINTS[endpoint]
    try:
        match method:
            case "GET":
                r = requests.get(url)
            case "POST":
                r = requests.post(url, json=payload)
            case "PUT":
                r = requests.put(url, json=payload)
            case "DELETE":
                r = requests.delete(url, json=payload)
            case _:
                print("método inválido")
                return
        print(f"\n{method} {url}")
        print("Response:", r.json())
    except Exception as e:
        print(f"Erro {method} {endpoint}: {e}")


def test_usuarios():
    print("\n=== TESTE USUARIOS ===")

    u1 = {"name": "maria", "password": "abc", "filial_id": 1, "isAdmin":False}
    u2 = {"name": "joao", "password": "123", "filial_id": 2, "isAdmin": True}
    u3 = {"name": "joao", "password": "999", "filial_id": 2, "isAdmin": False}

    req("POST", "usuarios", u1)
    req("POST", "usuarios", u2)
    req("POST", "usuarios", u3)

    req("GET", "usuarios")
    req("PUT", "usuarios", {"user_id": 1, "password": "nova", "filial_id": 2, "isAdmin": True})
    req("GET", "usuarios")

    req("DELETE", "usuarios", {"user_id": 1})
    req("GET", "usuarios")


def test_locais():
    print("\n=== TESTE LOCAIS ===")

    l1 = {"name": "salao", "location": "centro", "price": 200}
    l2 = {"name": "quadra", "location": "bairroA", "price": 100}
    l_dup = {"name": "salao", "location": "centro", "price": 300}

    req("POST", "locais", l1)
    req("POST", "locais", l2)
    req("POST", "locais", l_dup)  # conflito

    req("PUT", "locais", {"place_id": 1, "location": "bairroB", "price": 120})
    req("GET", "locais")

    req("DELETE", "locais", {"place_id": 1})
    req("GET", "locais")


def test_reservas():
    print("\n=== TESTE RESERVAS ===")

    r1 = {
        "user": "joao",
        "place_id": 1,
        "date_start": "01-02-2025",
        "date_end": "03-02-2025",
    }
    r_conflict = {
        "user": "joao",
        "place_id": 1,
        "date_start": "02-02-2025",
        "date_end": "05-02-2025",
    }
    r2 = {
        "user": "joao",
        "place_id": 1,
        "date_start": "10-03-2025",
        "date_end": "15-03-2025",
    }

    req("POST", "reservas", r1)
    req("POST", "reservas", r2)
    req("POST", "reservas", r_conflict)  # conflito

    req("GET", "reservas")

    req("PUT", "reservas", {
        "booking_id": 0,
        "place_id": 1,
        "date_start": "11-03-2025",
        "date_end": "20-03-2025",
    })

    req("GET", "reservas")

    req("DELETE", "reservas", {"booking_id": 1, "place_id": 1})
    req("GET", "reservas")


if __name__ == "__main__":
    test_usuarios()
    test_locais()
    test_reservas()

