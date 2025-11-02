from db.utils import normalizeString

users = [] # lista de todos os usuários
user_counter = 0

class User:
    def __init__(self, name, password, filial_id, isAdmin):
        global user_counter
        self.name = name
        self.password = password
        self.filial_id = filial_id
        self.isAdmin = isAdmin
        self.id = user_counter
        user_counter+=1

    def __str__(self):
        return f"{self.id}/{self.filial_id}: {self.name} ({'Admin' if self.isAdmin else 'User'})"

    def __repr__(self):
        return self.__str__()

#cria um usuario com nome, senha e se eh administrador ou nao
def create_user(**kwargs):
    user = User(**kwargs)
    users.append(user)
    return 0

#le um ou mais usuarios de acordo com os filtros de nome ou id
def read_user(byId=None, byName=None):
    #nenhum filtro de usuario, retorna todos
    if byId is None and byName is None:
        return users

    #filtra por id, retorna um User
    if byId is not None:
        return next((u for u in users if u.id == byId), None)
    #filtra por nome (substring normalizada), retorna lista de User
    else:
        byName = normalizeString(byName)
        return [u for u in users if byName and byName in normalizeString(u.name)]

#atualiza informacoes de um usuario
def update_user(**kwargs):
    user = read_user(byId=kwargs['user_id'])
    if not user:
        return 1
    for k, v in kwargs.items():
        if hasattr(user, k):
            setattr(user, k, v)
    return 0

#deleta um usuario
def delete_user(**kwargs):
    user = read_user(byId=kwargs['user_id'])
    if not user:
        return 1
    users.remove(user)
    return 0
