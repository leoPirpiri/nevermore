try:
    from base import Base, Stub
    from opinion import *
    from db_wrapper import get_comentario_pk
except:
    from .base import Base, Stub
    from .opinion import *

class Comment(Opinion):
    def __init__(self, *args, **kwargs):
        self.id_postagem = Stub()
        super().__init__(default_query=get_comentario_pk, *args, **kwargs)