from db.utils import normalizeString

places = []   # lista de todos os locais
place_counter = 0

class Place:
    def __init__(self, name, location, description, price, capacity, images):
        global place_counter
        self.name = name
        self.price = price
        self.location = location
        self.description = description
        self.images = images
        self.capacity = capacity
        self.id = place_counter
        place_counter+=1

    def __str__(self):
        return f"{self.id}: {self.name} - {self.location}"

    def __repr__(self):
        return self.__str__()

#cria um local disponivel para locacao
def create_place(**kwargs):
    p = Place(**kwargs)
    places.append(p)
    return 0

#retorna lista de Place a depender dos filtros utilizados (somente 1 filtro por vez)
def read_place(byName=None, byLocation=None, byId=None):
    if byName is not None:
        byName = normalizeString(byName)
        return [p for p in places if byName in normalizeString(p.name)]
    elif byLocation is not None:
        return [p for p in places if byLocation == normalizeString(p.location)]
    elif byId is not None:
        return next((p for p in places if byId == p.id), None)

    return places

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
places.append(Place("Teste 0", "Local 0", "um cu", 9.99, 4, ["chiyo.jpeg"]))
places.append(Place("Teste 1", "Local 1", "um krl", 23.4, 2, ["bagre.jpeg"]))
places.append(Place("Teste 2", "Local 2", "um kct", "2422.02", 1, ["chiyo.jpeg", "bagre.jpeg"]))
places.append(Place("Teste 3", "Local 3", "um kbr", 6.66, 7, ["bagre.jpeg","chiyo.jpeg"]))
places.append(Place("Nome Grandao hhuehue Teekçrv eriv psir vhste 4", "Localizacao eihr pep reh vp l N°4", "Descricao agavaasa  vkrdv paerivnrei viernvieri veirv iper vpie vriv erpuvher vue rvuh erovu ervu ergv ergv eurg voeg rvuoe grvouer vouer voug reouv oeu vrogveo rvouge rvo cu", "45.67", 69, ["chiyo.jpeg", "bagre.jpeg", "chiyo.jpeg", "chiyo.jpeg", "bagre.jpeg", "chiyo.jpeg", "bagre.jpeg", "bagre.jpeg", "chiyo.jpeg"]))
