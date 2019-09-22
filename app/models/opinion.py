try:
    from app.models.base import Base, Stub
    from app.models import db_wrapper
    #from app.models.db_wrapper import inserir_citacao, inserir_marcacao, inserir_topico, get_topico_pk, get_opinioes_topico_pk
except:
    from . import Base, Stub
    from . import db_wrapper
    #from .db_wrapper import inserir_citacao, inserir_marcacao, inserir_topico, get_topico_pk, get_opinioes_topico_pk

from datetime import datetime


class Opinion(Base):
    def __init__(self, id_post=None, *args, **kwargs):
        self.id_post = id_post
        self.texto = self.foto = self.dono = self.data_post = Stub()
        super().__init__(pk='id_post', *args, **kwargs)
    
    def get_dono(self):
        try:
            from app.models.user import User
        except:
            from .user import User as Usuario
        return Usuario(self.dono())


def _criar_opiniao(dados: dict, funcdb, marcados=[], topicos=[]) -> int:
    if dados['data_post'] is None:
        dados['data_post'] = datetime.now()
    p = funcdb(dados)[0]

    for marc in marcados:
        db_wrapper.inserir_marcacao({'id_post': p, 'id_usuario': marc.id_usuario()})
    for top in topicos:
        __criar_topico(top)
        db_wrapper.inserir_citacao({'id_post': p, 'nome_topico': top})

    return p

def __comment_post_wrapper(instancia={}):
    try:
        from app.models.post import Post as P
        from app.models.comment import Comment as C
    except:
        from .post import Post as P
        from .comment import Comment as C
    return C(instancia=instancia) if instancia['comentario'] else P(instancia=instancia)



def buscar_opinioes_por_topico(topico):
    ''' Retorna uma lista de Opiniões que estão marcados com o tópico especificado.
    '''
    return db_wrapper.get_opinioes_topico_pk(topico, autowrap=__comment_post_wrapper)