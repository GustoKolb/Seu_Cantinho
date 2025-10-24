import requests

# endereço do broker
BROKER_IP = "http://127.0.0.1:8000"

# '#define's para abstracao
# GET e POST = tipos de requisição
# RESERVAS = infos do cliente e do lugar de cada reserva
# LOCAIS = infos de todos os lugares
GET, POST, RESERVAS, LOCAIS = range(4)

def getTargetURL(target):
    if target == RESERVAS:
        url = "reservas"
    elif target == LOCAIS:
        url = "locais"
    else:
        url = ""

    return f"{BROKER_IP}/{url}"


# funcao geral pra enviar eventos
def send_request(request_type, request_target, args=None):
    target = getTargetURL(request_target);
        
    if request_type == GET:
        response = requests.get(target)
    elif request_type == POST:
        response = requests.post(target, json=args)
    else:#tirar esse else
        response = None
        print('seila poha')
    
    d={'method': "GET" if request_type == GET else "POST"}
    d.update(response.json())
    return d

if __name__ == "__main__":
    result = send_request(GET, RESERVAS);
    print(result)

    
    reserva = {
        'client_name':"nome do caba 1", #informacoes do cliente q alugou, dict()?
        'local_id': 1, #id do local reservado, eh +simples se cada lugar tiver um id unico
        #outras infos ai, ver coisa do pagamento lá
    }
    result = send_request(POST, RESERVAS, reserva);
    print(result)


    reserva = {
        'client_name':"nome do caba 2", #informacoes do cliente q alugou, dict()?
        'local_id': 2, #id do local reservado, eh +simples se cada lugar tiver um id unico
        #outras infos ai, ver coisa do pagamento lá
    }
    result = send_request(POST, RESERVAS, reserva);
    print(result)


    reserva = {
        'client_name':"nome do caba 3", #informacoes do cliente q alugou, dict()?
        'local_id': 1} #aqui tem q dar erro dps de implementar as regras de negocio
    result = send_request(POST, RESERVAS, reserva);
    print(result)


    result = send_request(GET, RESERVAS);
    print(result)
