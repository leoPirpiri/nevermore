try:
    from base import Base, Stub
    from opinion import *
    from db_wrapper import get_postagem_pk, get
except:
    from .base import Base, Stub
    from .opinion import *

class Post(Opinion):
    def __init__(self, *args, **kwargs):
        super().__init__(default_query=get_postagem_pk, *args, **kwargs)
    
    def get_comentarios(self):
        pass