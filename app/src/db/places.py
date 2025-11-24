from db.utils import normalizeString

places = []   # lista de todos os locais
place_counter = 0

class Place:
    def __init__(self, name, street, number, district, city, state, country,
                                         description, price, capacity, images):
        global place_counter
        self.id = place_counter
        place_counter += 1

        self.name = name
        self.street = street
        self.number = number
        self.district = district
        self.city = city
        self.state = state
        self.country = country
        self.description = description
        self.price = price
        self.capacity = capacity
        self.images = images

    def __str__(self):
        return f"{self.id}: {self.name} - {self.location}"

    def __repr__(self):
        return self.__str__()

#cria um local disponivel para locacao
def create_place(**kwargs):
    p = Place(**kwargs)
    places.append(p)
    return 0

def read_place(**f):
    if f.get("byId") is not None:
        return next((p for p in places if p.id == int(f["byId"])), [])

    results = places

    if f.get("byName") is not None:
        n = normalizeString(f["byName"])
        results = [p for p in results if n in normalizeString(p.name)]

    if f.get("byCountry") is not None:
        results = [p for p in results if p.country == f["byCountry"]]

    if f.get("byState") is not None:
        results = [p for p in results if p.state == f["byState"]]

    if f.get("byCity") is not None:
        results = [p for p in results if p.city == f["byCity"]]

    if f.get("byDistrict") is not None:
        results = [p for p in results if p.district == f["byDistrict"]]

    if f.get("byPriceMin") is not None:
        results = [p for p in results if p.price >= float(f["byPriceMin"])]

    if f.get("byPriceMax") is not None:
        results = [p for p in results if p.price <= float(f["byPriceMax"])]

    if f.get("byCapacityMin") is not None:
        results = [p for p in results if p.capacity >= int(f["byCapacityMin"])]

    if f.get("byCapacityMax") is not None:
        results = [p for p in results if p.capacity <= int(f["byCapacityMax"])]

    return results

def update_place(**kwargs):
    p = read_place(byId=kwargs['place_id'])
    if not p:
        return 1
    for k, v in kwargs.items():
        if hasattr(p, k):
            setattr(p, k, v)
    return 0

def delete_place(**kwargs):
    p = read_place(byId=kwargs['place_id'])
    if not p:
        return 1
    places.remove(p)
    return 0

#cria uns locais para teste
places.append(Place("Local Normal", "Rua A", "123", "Bairro B", "Cidade C", "Estado D", "País E", "Descrição normal", 50.0, 10, ["chiyo.jpeg"]))

places.append(Place("Extremamente Longo " * 10, "Rua X", "9999", "Bairro Y", "Cidade Z", "Estado W", "País V", "Descrição muito longa" * 20, 999999.99, 1000, ["chiyo.jpeg", "bagre.jpeg"]))

places.append(Place("Caracteres Especiais !@#$%^&*()", "Rúa ñ", "001", "Bairro *&^%", "Cítý Ç", "Estãdo", "Páis", "Descrição com símbolos ♥♦♣♠", 25.5, 5, ["bagre.jpeg"]))

places.append(Place("Unicode 👍", "Rua Emoji", "4", "Bairro 😎", "Cidade 🏙️", "Estado 🌍", "País ✈️", "Descrição com emojis 😁😂", 30.0, 12, ["chiyo.jpeg"]))
