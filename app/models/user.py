try:
    from base import Base, Stub
    from db_wrapper import get_usuario_pk, get_postagens_usuario_pk, get_seguindo_usuario_pk, get_seguidores_usuario_pk, get_bloqueados_usuario_pk
except:
    from . import Base, Stub
    from . import get_usuario_pk


class User(Base):
    def __init__(self, id_usuario=None, *args, **kwargs):
        self.id_usuario = id_usuario
        self.nome_usuario = self.nome_real = self.biografia = Stub()
        self.senha = self.foto = self.visibilidade = Stub()
        super().__init__(pk='id_usuario', default_query=get_usuario_pk, *args, **kwargs)

    def get_postagens(self):
        pass

    def get_seguindo(self):
        pass

    def get_seguidores(self):
        pass

    def get_bloqueados(self):
        pass