
class Stub:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Base:
    def __init__(self, pk=None, *args, **kwargs):
        if isinstance(pk, tuple) or isinstance(pk, list):
            self.pk_names = tuple(pk)
        else:
            self.pk_names = tuple([pk])
        for (k, v) in vars(self).items():
            if isinstance(v, Stub):
                vars(self)[k] = lambda t=k: self.query(t)
        super().__init__(*args, **kwargs)

    '''
    Tupla contendo os conteúdos das chaves primárias
    '''
    def pk(self):
        v = vars(self)
        return tuple(v[f] for f in self.pk_names)


    '''
    Wrapper para campos dinâmicos.
    Isto é, ao usar uma classe que herda desta, por exemplo, u = User(id_usuario=0),
    um campo só será solicitado ao BD se for explicitamente programado:
    u.nome_real()
    Em seguida, este método é invocado com parâmetro field='nome_real'.
    '''
    def _query(self, field):
        #print(field)
        pass
    

    '''
    Acessor absoluto
    '''
    def __get(self, nome, auto_call=True):
        r = vars(self)[nome]
        return r() if auto_call and callable(r) else r
    
    '''
    Modificador absoluto
    '''
    def __set(self, nome, val):
        vars(self)[nome] = val