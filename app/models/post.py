try:
    from app.models.base import Base, Stub
    from app.models.opinion import Opinion, _criar_opiniao
    from app.models import db_wrapper
    #from app.models.db_wrapper import get_postagem_pk, get_comentarios_postagem_pk, inserir_postagem
except:
    from .base import Base, Stub
    from .opinion import Opinion, _criar_opiniao
    from . import db_wrapper
    #from .db_wrapper import get_postagem_pk, get_comentarios_postagem_pk, inserir_postagem

class Post(Opinion):
    def __init__(self, id_post=None, *args, **kwargs):
        super().__init__(id_post=id_post, *args, **kwargs)
    
    def _default_query(self, field):
        return db_wrapper.get_postagem_pk(self.id_post())
    
    def get_comentarios(self):
        try:
            from app.models.comment import Comment as Comentario
        except:
            from .comment import Comment as Comentario
        return db_wrapper.get_comentarios_postagem_pk(self.id_post(), autowrap=Comentario)


def criar_post(texto, foto, dono, data=None, marcados=[], topicos=[]) -> Post:
    ''' Cria e registra um novo post no banco de dados.
    'dono' é do tipo User e 'marcados' é uma lista/iterável de User.
    'topicos' é uma lista de strings de tópicos marcados.
    'data' será a hora atual caso seja None.
    '''    
    d = {'texto': texto, 'foto': foto, 'dono': dono.id_usuario(), 'data_post': data}
    p = _criar_opiniao(d, db_wrapper.inserir_postagem, marcados, topicos)
    return Post(p)