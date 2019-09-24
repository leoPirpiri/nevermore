try:
    from app.models.base import Base, Stub
    from app.models import db_wrapper
    #from app.models.db_wrapper import get_notificao_pk, update_notificacao, inserir_notificacao
except:
    from . import Base, Stub
    from . import db_wrapper
    #from .db_wrapper import get_notificao_pk, update_notificacao, inserir_notificacao

from datetime import datetime

from enum import Enum
class NotificationType(Enum):
    NOVA_SOLICITACAO, NOVO_SEGUIDOR, ACEITA_SOLICITACAO, MARCACAO_POST = range(4)

class Notification(Base):
    def __init__(self, id_notificacao=None, *args, **kwargs):
        self.id_notificacao = id_notificacao
        self.tipo = self.lida = self.data_evento = Stub()
        self.dono_notificacao = self.mencionado = self.conteudo = Stub()
        super().__init__(pk='id_notificacao', *args, **kwargs)
    
    def _default_query(self, field):
        return db_wrapper.get_notificao_pk(self.id_notificacao())

    def marcar_lida(self):
        self._set('lida', True)
        d = self.to_dict()
        d['lida'] = True
        db_wrapper.update_notificacao(d)
    
    def get_dono(self):
        try:
            from app.models.user import User as Usuario
        except:
            from .user import User as Usuario
        return Usuario(self.dono())
    
    def get_mencionado(self):
        try:
            from app.models.user import User as Usuario
        except:
            from .user import User as Usuario
        return Usuario(self.mencionado())
    
    def get_conteudo(self):
        try:
            from app.models.post import Post as Postagem
        except:
            from .post import Post as Postagem
        return Postagem(self.conteudo())
    
    def get_tipo(self) -> NotificationType:
        return NotificationType(self.tipo())
    


def __criar_notif(d: dict, *args, **kwargs) -> Notification:
    du = {'lida': False, 'data_evento': datetime.now(), 'mencionado': None, 'conteudo': None}
    du.update(d)
    du.update(kwargs)
    return Notification(db_wrapper.inserir_notificacao(du)[0])


def criar_notificacao_usuario(dono, mencionado, tipo: NotificationType, *args, **kwargs) -> Notification:
    ''' Cria uma notificação relacionada a dois usuários (isto é, relações).
    'dono' (da notificação) e 'mencionado' são do tipo User.
    Parâmetros adicionais podem ser especificado, como conteudo, data e lida.
    '''
    d = { 'dono_notificacao': dono.id_usuario(), 'mencionado': mencionado.id_usuario(), 'tipo': tipo.value }
    return __criar_notif(d, *args, **kwargs)


def criar_notificacao_post(dono, conteudo, *args, **kwargs) -> Notification:
    ''' Cria uma notificação relacionada a um post (isto é, uma marcação).
    'dono' (da notificação) é do tipo User.
    'conteudo' é do tipo Opinion (ou int).
    Parâmetros adicionais podem ser especificado, como mencionado, tipo, data e lida.
    '''
    if not isinstance(conteudo, int):
        conteudo = conteudo.id_post()
    d = { 'dono_notificacao': dono.id_usuario(), 'conteudo': conteudo, 'tipo': NotificationType.MARCACAO_POST.value }
    return __criar_notif(d, *args, **kwargs)


def get_notificacoes_usuario(dono) -> [Notification]:
    ''' Obtém as notificações de um usuário.
    '''
    return db_wrapper.get_notificacoes_usuario_pk(dono.id_usuario(), autowrap=Notification)