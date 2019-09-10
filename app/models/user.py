from flask import g
try:
    from base import Base, Stub
except:
    from . import Base, Stub


class User(Base):
    def __init__(self, id_usuario=None, *args, **kwargs):
        self.id_usuario = id_usuario
        self.nome_usuario = self.nome_real = self.biografia = Stub()
        self.senha = self.foto = self.visibilidade = Stub()
        super().__init__(pk='id_usuario', *args, **kwargs)

