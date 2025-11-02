import unicodedata
from datetime import datetime

def parseDate(date_str):
    return datetime.strptime(date_str, "%d-%m-%Y")

#normaliza uma string em ascii minusculo
def normalizeString(string):
    if string is None:
        return None

    nfkd = unicodedata.normalize('NFKD', string)
    text = nfkd.encode('ASCII', 'ignore').decode('ASCII')
    return text.lower()
