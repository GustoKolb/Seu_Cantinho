import unicodedata

#normaliza uma string em ascii minusculo
def normalizeString(string):
    if string is None:
        return None

    nfkd = unicodedata.normalize('NFKD', string)
    text = nfkd.encode('ASCII', 'ignore').decode('ASCII')
    return text.lower()
