from db.utils import normalizeString
import base64

places = []   # lista de todos os locais
place_counter = 0

class Place:
    def __init__(self, name, street, number, district, city, state, country,
                                         description, price, capacity, image_b64=None, images=None):
        global place_counter
        self.id = place_counter
        place_counter += 1

        self.name = name
        self.country = country
        self.state = state
        self.city = city
        self.district = district
        self.street = street
        self.number = number
        self.description = description
        self.capacity = capacity
        self.price = price
        self.images = images
        if image_b64 is not None:
            self.setImage(image_b64)

    def setImage(self, b64_str):
        filepath = str(self.id)+'.jpg'
        self.images = [filepath]
        if ',' in b64_str:
            encoded_data = b64_str.split(',', 1)[-1]
        else:
            encoded_data = b64_str
        with open('db/images/'+filepath, '+wb') as f:
            f.write(base64.b64decode(encoded_data))

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
    p = read_place(byId=kwargs['id'])
    if not p:
        return 1

    kwargs.pop('id')
    for k, v in kwargs.items():
        if k == 'image_b64':
            p.setImage(v)
        if hasattr(p, k):
            setattr(p, k, v)
    return 0

def delete_place(**kwargs):
    p = read_place(byId=kwargs['id'])
    if not p:
        return 1
    places.remove(p)
    return 0


#carrega locais de exemplo

places.append(
    Place(
        name="Deck da Piscina",
        country="Brasil",
        state="SC",
        city="Florianópolis",
        district="Jurerê",
        street="Alameda dos Mares",
        number="50",
        description="Área externa com deck e piscina infinita.",
        capacity=80,
        price=3200.00,
        images=['0.jpg'],
    )
)

places.append(
    Place(
        name="Estúdio Urbano",
        country="Brasil",
        state="PR",
        city="Curitiba",
        district="Batel",
        street="Rua Visconde de Guarapuava",
        number="4550",
        description="Loft moderno para ensaios fotográficos e pequenas reuniões.",
        capacity=30,
        price=1200.00,
        images=['1.jpg'],
    )
)

places.append(
    Place(
        name="Sala de Reuniões",
        country="Brasil",
        state="GO",
        city="Goiânia",
        district="Setor Marista",
        street="Avenida do Contorno",
        number="120",
        description="Sala profissional com projetor e Wi-Fi de alta velocidade.",
        capacity=15,
        price=600.00,
        images=['3.jpg'],
    ))
