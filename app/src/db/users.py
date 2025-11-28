from db.utils import normalizeString

users = [] # lista de todos os usuários
user_counter = 0

class User:
    def __init__(self, name, password, filial_id, isAdmin):
        global user_counter
        self.id = user_counter
        user_counter+=1
        self.name = name
        self.password = password
        self.filial_id = filial_id
        self.isAdmin = isAdmin

#cria um usuario com nome, senha e se eh administrador ou nao
def create_user(**kwargs):
    user = User(**kwargs)
    users.append(user)
    return 0

#le um ou mais usuarios de acordo com os filtros passados
def read_user(**f):
    byId   = f.get("byId")
    byName = f.get("byName")
    byPassword = f.get("byPassword")

    if byId is None and byName is None:
        return users

    if byId is not None:
        return next((u for u in users if u.id == int(byId)), [])
    
    #pesquisa qualquer por substring de nome
    if byName is not None and byPassword is None:
        byNameNorm = normalizeString(byName)
        return [u for u in users if byNameNorm in normalizeString(u.name)]
    
    #caso de login
    if byName is not None and byPassword is not None:
        return [u for u in users if byName == u.name and byPassword == u.password]

#atualiza informacoes de um usuario
def update_user(**kwargs):
    user = read_user(byId=kwargs['id'])
    if not user:
        return 1

    kwargs.pop('id')
    for k, v in kwargs.items():
        if hasattr(user, k):
            setattr(user, k, v)
    return 0

#deleta um usuario
def delete_user(**kwargs):
    user = read_user(byId=kwargs['id'])
    if not user:
        return 1
    users.remove(user)
    return 0

#cria usuario administrador padrao
users.append(User("admin", "admin", 0, True))
users.append(User("normal", "normal", 0, False))
