try:
    from . import Base, Stub
    from . import get_usuario_pk, get_usuario_nome_usuario, get_postagens_usuario_pk, get_seguindo_usuario_pk, get_seguidores_usuario_pk, get_bloqueados_usuario_pk
except:
    from base import Base, Stub
    from db_wrapper import get_usuario_pk, get_usuario_nome_usuario, get_postagens_usuario_pk, get_seguindo_usuario_pk, get_seguidores_usuario_pk, get_bloqueados_usuario_pk


"""
Classe Usuário.
"""
class User(Base):
    '''
    Construtor de Usuário.
    Forneça a chave primária em id_usuario; ou ainda declare id_usuario=None e nome_usuario={id do usuário}.
    '''
    def __init__(self, id_usuario=None, *args, **kwargs):
        self.id_usuario = id_usuario
        self.nome_usuario = self.nome_real = self.biografia = Stub()
        self.senha = self.foto = self.visibilidade = Stub()

        if id_usuario is None and 'nome_usuario' in kwargs:
            kwargs['instancia'] = get_usuario_nome_usuario(kwargs['nome_usuario'])
            self.id_usuario = kwargs['instancia']['id_usuario']
            
        super().__init__(pk='id_usuario', default_query=get_usuario_pk, *args, **kwargs)

    def get_postagens(self):
        pass

    def get_seguindo(self):
        pass

    def get_seguidores(self):
        pass

    def get_bloqueados(self):
        pass