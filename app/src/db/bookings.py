from db.utils import normalizeString, parseDate

bookings = []
booking_counter = 0

class Booking:
    def __init__(self, user, place_id, date_start, date_end):
        global booking_counter
        self.user = user#client
        self.place_id = place_id
        self.date_start = parseDate(date_start)
        self.date_end = parseDate(date_end)
        self.booking_id = booking_counter
        booking_counter+=1

    def __str__(self):
        return f"{self.user} {self.place_id} {self.date_start} | {self.date_end}"

    def __repr__(self):
        return self.__str__()

def date_conflict(d1_start, d1_end, d2_start, d2_end):
    return not (d1_end <= d2_start or d1_start >= d2_end)

def create_booking(**kwargs):
    required = ["user", "place_id", "date_start", "date_end"]
    if not all(k in kwargs for k in required):
        return None
    
    kw_date_start = parseDate(kwargs['date_start'])
    kw_date_end = parseDate(kwargs['date_end'])
    if any(b.place_id == kwargs["place_id"] and date_conflict(b.date_start, b.date_end,
                                    kw_date_start, kw_date_end) for b in bookings):
        return 1

    b = Booking(**kwargs)
    bookings.append(b)
    return 0

# lê reservas de acordo com filtros (user, name, byId)
def read_booking(byId=None, byUser=None, byName=None):
    # se for filtrado por id, retorna único Booking
    if byId is not None:
        return next((b for b in bookings if b.booking_id == byId), None)

    # filtra por user e name, retorna lista
    result = []
    byUser = normalizeString(byUser)
    byName = normalizeString(byName)
    for b in bookings:
        if byUser and b.user.name != byUser:
            continue
        if byName and b.place.name != byName:
            continue
        result.append(b)
    return result

# atualiza uma reserva
def update_booking(**kwargs):
    booking = read_booking(byId=kwargs["booking_id"])
    if not booking:
        return 1

    kw_date_start = parseDate(kwargs['date_start'])
    kw_date_end = parseDate(kwargs['date_end'])
    if any(b.place_id == kwargs["place_id"] and date_conflict(b.date_start, b.date_end,
                                    kw_date_start, kw_date_end) for b in bookings):
        return 1

    for k, v in kwargs.items():
        if hasattr(booking, k):
            setattr(booking, k, v)
    return 0

def delete_booking(**kwargs):
    booking = read_booking(byId=kwargs['booking_id'])
    if not booking:
        return 1
    bookings.remove(booking)
    return 0
