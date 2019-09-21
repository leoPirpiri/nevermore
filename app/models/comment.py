try:
    from app.models.base import Base, Stub
    from app.models.opinion import Opinion, _criar_opiniao
    from app.models import db_wrapper
    #from app.models.db_wrapper import get_comentario_pk, inserir_comentario
except:
    from .base import Base, Stub
    from .opinion import Opinion, _criar_opiniao
    from . import db_wrapper
    #from .db_wrapper import get_comentario_pk

class Comment(Opinion):
    def __init__(self, id_post=None, *args, **kwargs):
        self.id_postagem = Stub()
        super().__init__(id_post=id_post, *args, **kwargs)
    
    def _default_query(self, field):
        return db_wrapper.get_comentario_pk(self.id_post())
    
    def get_postagem(self):
        try:
            from app.models.post import Post as Postagem
        except:
            from .post import Post as Postagem
        return Postagem(self.id_postagem())


def criar_comentario(texto, foto, dono, post, data=None, marcados=[], topicos=[]) -> Comment:
    ''' Cria e registra um novo comentário no banco de dados.
    'dono' é do tipo User e 'marcados' é uma lista/iterável de User.
    'topicos' é uma lista de strings de tópicos marcados.
    'post' é do tipo Post/Opinião.
    'data' será a hora atual caso seja None.
    '''    
    d = {'texto': texto, 'foto': foto, 'dono': dono.id_usuario(), 'data_post': data, 'post': post.id_post()}
    p = _criar_opiniao(d, db_wrapper.inserir_comentario, marcados, topicos)
    return Comment(p)