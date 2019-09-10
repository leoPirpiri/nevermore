from flask import g
try:
    from base import Base, Stub
    from opinion import *
except:
    from .base import Base, Stub
    from .opinion import *

class Post(Opinion):
    def __init__(self, *args, **kwargs):
        self.id_postagem = Stub()
        super().__init__(*args, **kwargs)