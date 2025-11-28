from db.utils import normalizeString, date_conflict
from db.places import read_place

bookings = []
booking_counter = 0

class Booking:
    def __init__(self, client_name, client_email, client_phone, amount_paid, total_amount, place, start_date, end_date):
        global booking_counter
        self.id = booking_counter
        booking_counter+=1

        self.client_name = client_name
        self.client_email = client_email
        self.client_phone = client_phone
        self.amount_paid = amount_paid
        self.total_amount = total_amount
        self.place = place
        self.start_date = start_date
        self.end_date = end_date

def create_booking(**kwargs):
    if any([b.place.id == int(kwargs['place_id']) and date_conflict(b.start_date, b.end_date,
                    kwargs['start_date'], kwargs['end_date']) for b in bookings]):
        return 1

    #troca id por referencia ao objeto inteiro
    place = read_place(byId=kwargs['place_id']) 
    kwargs.pop('place_id')
    kwargs["place"] = place

    b = Booking(**kwargs)
    bookings.append(b)
    return 0

# lê reservas de acordo com filtros (client, name, byId)
def read_booking(**f):
    byId   = f.get("byId")
    byClientName = f.get("byClientName")
    byPlaceId = f.get("byPlaceId")

    if byId is not None:
        return next((b for b in bookings if b.id == int(byId)), [])

    result = []
    client_name = normalizeString(byClientName)

    for b in bookings:
        if client_name and normalizeString(b.client_name) != client_name:
            continue
        if byPlaceId and b.place.id != int(byPlaceId):
            continue
        result.append(b)

    return result

# atualiza uma reserva
def update_booking(**kwargs):
    booking = read_booking(byId=kwargs["id"])
    if not booking:
        return 1

    if any([b.id != int(kwargs['id']) and b.place.id == int(kwargs['place_id']) and date_conflict(
            b.start_date, b.end_date, kwargs['start_date'], kwargs['end_date']) for b in bookings]):
        return 1

    kwargs.pop('id')
    for k, v in kwargs.items():
        if hasattr(booking, k):
            if k == 'place_id':
                v = read_place(byId = v) 
                setattr(booking, 'place', v)
            else:
                setattr(booking, k, v)
    return 0

def delete_booking(**kwargs):
    booking = read_booking(byId=kwargs['id'])
    if not booking:
        return 1
    bookings.remove(booking)
    return 0
