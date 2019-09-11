
class Stub:
    def __init__(self, *args, **kwargs):
        pass


'''
Classe base para Entidades Notáveis do Banco de Dados.
Especialmente útil para aquelas entidades que serão obtidas individualmente.
Usualmente recebe como parâmetro pk, uma tupla de string que indicam as colunas que são chaves primárias.
Esse comportamento é sobrecarregado pelas classes que implementam esta.
Essas classes podem descrever campos dos métodos iguais a uma instância de Stub antes da chamada deste construtor;
nesse caso, esses campos são encapsulados para ser obtido dinâmicamente do banco de dados.
Esses stubs podem ser acessados por meio de (Base)._stubs;
Além disso, passando um dicionário 'instancia' em um construtor de qualquer classe que implementa esta, inicializará
os campos com os valores descritos no dicionário.
Finalmente, passando 'default_query' no construtor, define-se uma função padrão para obter a query por meio de stubs,
usualmente alguma função de db_wrapper.
'''
class Base:
    def __init__(self, pk=None, *args, **kwargs):

        # Trata e obtém a tupla de chaves primárias
        if isinstance(pk, tuple) or isinstance(pk, list):
            self.pk_names = tuple(pk)
        else:
            self.pk_names = tuple([pk])
        
        # Query padrão
        self._default_query = kwargs.get('default_query', None)

        # Armazena quais colunas são stubs
        self._stubs = set()
        # Converte todos os stubs em auto-querys.
        for (k, v) in vars(self).items():
            if isinstance(v, Stub):
                self._stubs.add(k)
                vars(self)[k] = lambda t=k: self._query(t)
        
        # Atualiza os campos das chaves primárias, para termos certeza de que são invocaveis
        # i.e., deixar consistente com as outras colunas.
        self.__update_fields(dict([(n, self.__get(n, False)) for n in self.pk_names]))
        
        # Inicializador de instância
        if 'instancia' in kwargs:
            cp_stubs = set(self._stubs)
            self._stubs.update(self.pk_names)
            self.__update_stubs(kwargs['instancia'])
            self._stubs = cp_stubs

    '''
    Tupla contendo os conteúdos das chaves primárias
    '''
    def pk(self):
        return tuple(self.__get(f) for f in self.pk_names)


    '''
    Wrapper para campos dinâmicos.
    Isto é, ao usar uma classe que herda desta, por exemplo, u = User(id_usuario=0),
    um campo só será solicitado ao BD se for explicitamente programado:
    u.nome_real()
    Em seguida, este método é invocado com parâmetro field='nome_real'.
    Espera-se que retorne o valor do campo solicitado.
    '''
    def _query(self, field):
        if not self._default_query is None:
            self.__update_stubs(self._default_query(field))
        return self.__get(field, auto_call=False)

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
        vars(self)[nome] = val if callable(val) else lambda v=val: v
    
    '''
    Função auxiliar opcional.
    Dado um dicionário de field->valor, atualiza a classe.
    Utiliza o método __set.
    '''
    def __update_fields(self, fielddict: dict):
        for k, v in fielddict.items():
            self.__set(k, v)
    
    '''
    Função auxiliar opcional.
    Dado um dicionário de stubs->valor, atualiza a classe.
    Qualquer stub não declarado em self._stubs é ignorado.
    Utiliza o método __set.
    '''
    def __update_stubs(self, stubdict: dict):
        return self.__update_fields(dict([(i, stubdict[i]) for i in self._stubs.intersection(stubdict)]))