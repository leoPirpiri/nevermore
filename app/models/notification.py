try:
    from base import Base, Stub
except:
    from . import Base, Stub


class Notification(Base):
    def __init__(self, id_notificacao=None, *args, **kwargs):
        self.id_notificacao = id_notificacao
        self.tipo = self.lida = self.data_evento = Stub()
        self.dono_notificacao = self.mencionado = self.conteudo = Stub()
        super().__init__(pk='id_notificacao', *args, **kwargs)

    def marcar_lida(self):
        pass