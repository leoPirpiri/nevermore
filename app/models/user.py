try:
    from app.models.base import Base, Stub
    from app.models.post import Post as Postagem
    from app.models.notification import criar_notificacao_usuario, NotificationType as NotifType
    from app.models import db_wrapper
    #from app.models.db_wrapper import get_usuario_pk, get_usuario_nome_usuario, get_postagens_usuario_pk, get_seguindo_usuario_pk, get_seguidores_usuario_pk, get_bloqueados_usuario_pk, get_relacao_usuario_pk, update_usuario, update_relacao_usuario, inserir_relacao, inserir_usuario, get_usuarios_busca
except:
    from .base import Base, Stub
    from .post import Post as Postagem
    from .notification import Notification
    from . import db_wrapper
    #from .db_wrapper import get_usuario_pk, get_usuario_nome_usuario, get_postagens_usuario_pk, get_seguindo_usuario_pk, get_seguidores_usuario_pk, get_bloqueados_usuario_pk, get_relacao_usuario_pk, update_usuario, update_relacao_usuario, inserir_relacao, inserir_usuario, get_usuarios_busca


from enum import Enum
class Relacionamento(Enum):
    SEGUINDO, SOLICITOU, BLOQUEOU, BLOQUEADO, NONE = range(5)

class User(Base):
    """
    Classe Usuário.
    """

    def __init__(self, id_usuario: int = None, *args, **kwargs):
        '''
        Construtor de Usuário.
        Forneça a chave primária em id_usuario; ou ainda declare id_usuario=None e nome_usuario={username}.
        '''
        self.id_usuario = id_usuario
        self.nome_usuario = self.nome_real = self.biografia = Stub()
        self.senha = self.foto = self.visibilidade = self.cont_seguidores = Stub()

        if id_usuario is None and 'nome_usuario' in kwargs:
            inst = db_wrapper.get_usuario_nome_usuario(kwargs['nome_usuario'])
            if not inst is None:
                self.id_usuario = inst['id_usuario']
                kwargs['instancia'] = inst

        super().__init__(pk='id_usuario', *args, **kwargs)

    def _default_query(self, field):
        r = db_wrapper.get_usuario_pk(self.id_usuario())
        return r

    def get_postagens(self):
        return db_wrapper.get_postagens_usuario_pk(self.id_usuario(), autowrap=Postagem)

    def get_seguindo(self):
        return db_wrapper.get_seguindo_usuario_pk(self.id_usuario(), autowrap=User)

    def get_seguidores(self):
        return db_wrapper.get_seguidores_usuario_pk(self.id_usuario(), autowrap=User)

    def get_bloqueados(self):
        return db_wrapper.get_bloqueados_usuario_pk(self.id_usuario(), autowrap=User)
    
    def __existe_relacionamento(self, usuario_alvo: 'User'):
        return db_wrapper.get_relacao_usuario_pk(self.id_usuario(), usuario_alvo.id_usuario())
    
    def get_relacionamento(self, usuario_alvo: 'User', r=None) -> Relacionamento:
        ''' Obtém uma instância de Relacionamento
        '''
        r = r or self.__existe_relacionamento(usuario_alvo)
        return Relacionamento.NONE if r is None else Relacionamento(r['tipo'])
    
    def _set_relacionamento(self, usuario_alvo: 'User', relacao: Relacionamento):
        ''' Atualiza o relacionamento entre os usuários.
        Atualiza também o contador de seguidores:
        Isto é, se o novo ou o anterior relacionamento for do tipo seguindo, o contador é atualizado.
        (A atualização é completa, para garantir a integridade do banco de dados).
        '''
        rold = self.__existe_relacionamento(usuario_alvo)
        opr = db_wrapper.inserir_relacao if rold is None else db_wrapper.update_relacao_usuario
        rold = self.get_relacionamento(usuario_alvo, rold)
        opr({'tipo': relacao.value, 'origem': self.id_usuario(), 'alvo': usuario_alvo.id_usuario()})
        
        if rold == Relacionamento.SEGUINDO or relacao == Relacionamento.SEGUINDO:
            self.atualizar_dados_usuario(upd_cont_seguidores=True)
    
    def solicitar_seguir(self, solicitante: 'User') -> Relacionamento:
        ''' Solicita este usuário para o seguir (como solicitante).
        Retorna o novo relacionamento (tipo user.Relacionamento).
        Isto é, se a solicitação foi aceita automaticamente (perfil público), ou está para ser aprovada.
        Envia as notificações necessárias.
        '''
        rold = solicitante.get_relacionamento(self)

        # Não faz nada se eles não tem relacionamento
        if not rold is Relacionamento.NONE:
            return rold
        
        # perfil público
        if self.visibilidade():
            rargs = (Relacionamento.SEGUINDO, NotifType.NOVO_SEGUIDOR)
        else:
            rargs = (Relacionamento.SOLICITOU, NotifType.NOVA_SOLICITACAO)
        solicitante._set_relacionamento(self, rargs[0])
        criar_notificacao_usuario(self, solicitante, rargs[1])
        return rargs[0]
    
    def bloquear(self, bloqueante: 'User') -> Relacionamento:
        ''' O bloqueante (tipo User) bloqueia este usuário.
        Retorna o antigo relacionamento que este usuário tinha com bloqueante.
        (Isto é, para saber se o alvo do bloqueio tbm tinha bloqueado o infeliz).
        '''
        bloqueante._set_relacionamento(self, Relacionamento.BLOQUEOU)
        rold = self.get_relacionamento(bloqueante)
        if not rold is Relacionamento.BLOQUEOU:
            self._set_relacionamento(bloqueante, Relacionamento.BLOQUEADO)
        return rold
    
    def desbloquear(self, desbloqueante: 'User') -> Relacionamento:
        ''' O desbloqueante (tipo User) desbloqueia este usuário.
        Retorna o relacionamento que este usuário passará a ter com desbloqueante:
        Isto é, se este usuário também bloqueou o bloqueante, retorna BLOQUEOU.
        Senão, retorna NONE.
        '''
        rold = self.get_relacionamento(desbloqueante)
        if rold is Relacionamento.BLOQUEOU:
            desbloqueante._set_relacionamento(self, Relacionamento.BLOQUEADO)
            #self._set_relacionamento(desbloqueante, Relacionamento.BLOQUEOU)
            return Relacionamento.BLOQUEOU
        else:
            desbloqueante._set_relacionamento(self, Relacionamento.NONE)
            self._set_relacionamento(desbloqueante, Relacionamento.NONE)
            return Relacionamento.NONE

    def atualizar_dados_usuario(self, dados:dict = None, upd_cont_seguidores=True):
        ''' Atualize os dados do usuário por meio da classe ou passando dados: dict como argumento.
        Se 'upd_cont_seguidores' for True, então uma query adicional é feita para atualizar o contador de seguidores.
        '''
        d = self.to_dict() if dados is None else dados
        if upd_cont_seguidores:
            d['cont_seguidores'] = len(self.get_seguidores())
        d['id_usuario'] = self.id_usuario()
        db_wrapper.update_usuario(d)
        self._update_fields(self._default_query(None))
    
    def e_valido(self):
        ''' Método boilerplate para verificar se uma instância é válida.
        '''
        return not self.pk()[0] is None


def get_user(nome_usuario) -> User:
    ''' Obtém uma instância de usuário para um dado nome.
    Retorna None caso o usuário não exista.
    '''
    u = User(nome_usuario=nome_usuario)
    return u if u.e_valido() else None



def registrar_usuario(dados: dict, lazy: bool = True) -> 'User':
    ''' Registra um novo usuário no sistema.
    Recebe um dicionário como parâmetro que contém os campos necessários.
    Se lazy=True, então retorna uma instância preguiçosa de Usuário.
    Do contrário, inicializa-o com as informações contidas em 'dados' (Menos seguro).
    '''
    d = {'biografia': "", "foto": "", "visibilidade": True, "nome_real": "", "senha": ""}
    d.update(dados)
    q = db_wrapper.inserir_usuario(d)[0]
    return User(q) if lazy else User(q, instancia=dados)

def buscar_usuarios_por_string(occur):
    ''' Busca uma lista de usuário que possuem a string de ocorrência na biografia, nome ou nome completo.
    '''
    return db_wrapper.get_usuarios_busca(occur, autowrap=User)

def aceitar_solicitacao(pedinte: User, alvo: User):
    ''' Se houver uma solicitação de seguimento de pedinte para alvo, então aceita-a.
    Avisa ao usuário pedinte que sua solicitação foi aceita.
    '''
    if pedinte.get_relacionamento(alvo) is Relacionamento.SOLICITOU:
        pedinte._set_relacionamento(alvo, Relacionamento.SEGUINDO)
        criar_notificacao_usuario(pedinte, alvo, NotifType.ACEITA_SOLICITACAO)