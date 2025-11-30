import unicodedata
from datetime import datetime

DATE_FORMAT = "%d-%m-%Y"

#recebe quatro string de data em dmy e verifica se ha sobreposicao
def date_conflict(d1_start_str, d1_end_str, d2_start_str, d2_end_str):
    d2_start = datetime.strptime(d2_start_str, DATE_FORMAT)
    d2_end = datetime.strptime(d2_end_str, DATE_FORMAT)
    d1_start = datetime.strptime(d1_start_str, DATE_FORMAT)
    d1_end = datetime.strptime(d1_end_str, DATE_FORMAT)

    return d2_start <= d1_end and d2_end >= d1_start

#normaliza uma string em ascii minusculo
def normalizeString(string):
    if string is None:
        return None

    nfkd = unicodedata.normalize('NFKD', string)
    text = nfkd.encode('ASCII', 'ignore').decode('ASCII')
    return text.lower()
