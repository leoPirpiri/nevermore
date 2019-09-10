from flask import g
try:
    from base import Base, Stub
    from opinion import *
except:
    from .base import Base, Stub
    from .opinion import *

class Comment(Opinion):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)