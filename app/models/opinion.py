from flask import g
try:
    from base import Base, Stub
except:
    from . import Base, Stub

class Opinion(Base):
    def __init__(self, id_post=None, *args, **kwargs):
        self.id_post = id_post
        self.texto = self.foto = self.dono = self.data_post = Stub()
        super().__init__(pk='id_post', *args, **kwargs)