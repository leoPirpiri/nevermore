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
        self.texto = self.foto = self.dono = self.data_post = self.excluido = Stub()
        super().__init__(pk='id_post', *args, **kwargs)
    
    def get_dono(self):
        if not hasattr(self, '__tmp_dono'):
            try:
                from app.models.user import User as Usuario
            except:
                from .user import User as Usuario
            self.__tmp_dono = Usuario(self.dono())
        return self.__tmp_dono
    
    def visivel_para(self, alvo):
        ''' Retorna True se o post é visível para o usuário alvo.
        'alvo' é do tipo User.
        '''
        if self.excluido():
            return False
        
        if alvo.id_usuario() == self.get_dono().id_usuario():
            return True

        try:
            from app.models.user import Relacionamento
        except:
            from .user import Relacionamento
        
        relacao = alvo.get_relacionamento(self.get_dono())

        if relacao is Relacionamento.BLOQUEADO or relacao is Relacionamento.BLOQUEOU:
            return False
        
        if not self.get_dono().visibilidade() and not relacao is Relacionamento.SEGUINDO:
            return False

        return True
    
    def visivel_para_mim(self):
        ''' Retorna True se o post é visível para o usuário alvo.
        Usa uma rotina do Flask (i.e. um método controller-dependent)
        '''
        from flask import g
        return self.visivel_para(g.user)


def __criar_topico(nome_topico):
    if db_wrapper.get_topico_pk(nome_topico) is None:
        db_wrapper.inserir_topico({'nome_topico': nome_topico})


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


def buscar_trend_topics():
    return db_wrapper.get_trend_topics()

