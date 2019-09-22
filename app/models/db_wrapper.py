'''
Este módulo contém os SQLs e funções usuais de acesso ao BD.
'''




from functools import wraps

import click
import psycopg2
import psycopg2.extras
from flask import current_app, g, has_request_context
from flask.cli import with_appcontext



__tmp_conn = None
__tmp_cur = None

def commit_changes(force=False):
    global __tmp_conn, __tmp_cur
    if not has_request_context() and not __tmp_conn is None:
        __tmp_conn.commit()
    elif 'dba' in g and force:
        g.dba.commit()

def get_db(discardPrevious=False) -> psycopg2.extras.DictCursor:
    global __tmp_conn, __tmp_cur
    """Obtém e levanta, se necessário, uma conexão ao banco de dados.
    """

    # Caso não esteja usando Flask
    if not has_request_context():
        if __tmp_conn is None:
            __tmp_conn = psycopg2.connect(dbname="projbd", user="leandro", password='Invited,')
        if __tmp_cur is None:
            __tmp_cur = __tmp_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return __tmp_cur
    
    if 'dba' not in g:
        g.dba = psycopg2.connect(dbname="projbd", user="leandro", password='Invited,')
    if 'cur' not in g:
        g.cur = g.dba.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    if discardPrevious:
        g.cur.close()
        g.cur = g.dba.cursor(cursor_factory=psycopg2.extras.DictCursor)

    return g.cur


def close_cur(e=None):
    """If this request connected to the database, close the
    connection.
    """
    commit_changes(True)

    cur = g.pop('db', None)
    if cur is not None:
        cur.close()
    
    conn = g.pop('conn', None)
    if conn is not None:
        conn.commit()
        conn.close()


def get_base_schema():
    if has_request_context():
        with current_app.open_resource('models/base.sql') as f:
            r = f.read().decode('utf8')
    else:
        with open('app/models/base.sql', 'r') as f:
            r = f.read()
    return r







def __impl_default_fetch(r, one=True):
    cur = get_db()
    p = r[1] if hasattr(r[1], '__iter__') and not isinstance(r[1], str) else [r[1]]
    cur.execute(r[0], p)
    if not one is None:
        return cur.fetchone() if one else cur.fetchall()

'''
Magia negra: Faz uma consulta ao Banco de Dados.
Retorna um dicionário da biblioteca (se o argumento todict=True for fornecido, retorna um dicionário nativo do Python)
'''
def default_fetch_one(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        todict = kwargs.pop('todict', False)
        autowrap = kwargs.pop('autowrap', None)
        r = fn(*args, **kwargs)
        rt = __impl_default_fetch(r)
        if callable(autowrap):
            return autowrap(instancia=dict(rt))
        else:
            return dict(rt) if todict else rt
    return wrapped

'''
Magia negra: Faz uma consulta ao Banco de Dados.
Retorna uma lista da biblioteca (se o argumento todict=True for fornecido, retorna uma lista nativa do Python)
'''
def default_fetch_many(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        todict = kwargs.pop('todict', False)
        autowrap = kwargs.pop('autowrap', None)
        r = fn(*args, **kwargs)
        rt = __impl_default_fetch(r, False)
        if callable(autowrap):
            return [autowrap(instancia=dict(i)) for i in rt]
        else:
            return [dict(i) for i in rt] if todict else rt
    return wrapped

'''
Magia negra: Faz uma operação no Banco de Dados.
'''
def default_fetch_none(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        rt = __impl_default_fetch(fn(*args, **kwargs), None)
    return wrapped






'''
-------------------------
SELECTS!
-------------------------
'''



'''
Retorna um dicionário para uma instância de usuário.
'''
@default_fetch_one
def get_usuario_pk(id_usuario):
    return ('SELECT * FROM usuario WHERE id_usuario = %s', id_usuario)

'''
Retorna um dicionário para uma instância de usuário.
'''
@default_fetch_one
def get_usuario_nome_usuario(nome_usuario):
    return ('SELECT * FROM usuario WHERE nome_usuario = %s', nome_usuario)


'''
Retorna um dicionário para uma instância de Notificação.
'''
@default_fetch_one
def get_notificao_pk(id_notificacao):
    return ('SELECT * FROM notificacao WHERE id_notificacao = %s', id_notificacao)


'''
Retorna um dicionário para uma instância de Postagem.
'''
@default_fetch_one
def get_postagem_pk(id_post):
    return ('SELECT * FROM opiniao WHERE id_post = %s', id_post)


'''
Retorna um dicionário para uma instância de Comentário.
'''
@default_fetch_one
def get_comentario_pk(id_post):
    return ('SELECT * FROM opiniao INNER JOIN comentario ON opiniao.id_post = comentario.id_post WHERE comentario.id_post = %s', id_post)



'''
Retorna um dicionário para uma relação entre dois usuários.
Recebe um dicionário que representa o objeto.
Consulte update_relacao_usuario_pk.
'''
@default_fetch_many
def get_relacao_usuario_obj(p):
    return ('SELECT * FROM relacao WHERE origem = %(origem)s AND alvo = %(alvo)s', p)

'''
Retorna um dicionário para uma relação entre dois usuários.
Retorna None caso não exista tal relacionamento.
Consulte update_relacao_usuario_pk.
'''
def get_relacao_usuario_pk(origem, alvo):
    r = get_relacao_usuario_obj({'origem': origem, 'alvo': alvo})
    return None if len(r) == 0 else r[0]

'''
Retorna um dicionário para um tópico.
'''
@default_fetch_one
def get_topico_pk(nome_topico):
    return ('SELECT * FROM topico WHERE nome_topico = %s', nome_topico)


'''
Retorna um dicionário para os tópicos do momento.
'''
@default_fetch_one
def get_topicos_trends():
    return ( """SELECT count(top.nome_topico) as quan, top.nome_topico as nome
                FROM public.citacao_topico as cit,
                     public.topico as top,
                     public.opiniao as op
                WHERE cit.id_post = op.id_post
                     and cit.nome_topico = top.nome_topico
                     and (DATE_PART('day', now()::timestamp - op.data_post::timestamp) * 24 + 
                              DATE_PART('hour', now()::timestamp - op.data_post::timestamp)) < 4
                group by (top.nome_topico, top.nome_topico)
                order by quan desc
                limit 10;""")


'''
Retorna uma lista de dicionários de notificações do usuário.
'''
@default_fetch_many
def get_notificacoes_usuario_pk(id_usuario):
    return ('SELECT * FROM notificacao WHERE dono_notificacao = %s ORDER BY data_evento DESC', [id_usuario])

'''
Retorna uma lista de dicionários de postagens do usuário.
'''
@default_fetch_many
def get_postagens_usuario_pk(id_usuario):
    return ('SELECT * FROM opiniao INNER JOIN postagem ON opiniao.id_post = postagem.id_post WHERE opiniao.dono = %s ORDER BY opiniao.data_post DESC', [id_usuario])

'''
Retorna uma lista de dicionários de usuários que este usuário segue.
'''
@default_fetch_many
def get_seguindo_usuario_pk(id_usuario):
    return ('SELECT * FROM relacao INNER JOIN usuario ON usuario.id_usuario = relacao.alvo WHERE relacao.tipo = 0 AND relacao.origem = %s', [id_usuario])

'''
Retorna uma lista de dicionários de usuários que este usuário solicitou para seguir.
'''
@default_fetch_many
def get_solicitou_seguir_usuario_pk(id_usuario):
    return ('SELECT * FROM relacao INNER JOIN usuario ON usuario.id_usuario = relacao.alvo WHERE relacao.tipo = 1 AND relacao.origem = %s', [id_usuario])

'''
Retorna uma lista de dicionários de usuários que este usuário bloqueou.
'''
@default_fetch_many
def get_bloqueados_usuario_pk(id_usuario):
    return ('SELECT * FROM relacao INNER JOIN usuario ON usuario.id_usuario = relacao.alvo WHERE relacao.tipo = 2 AND relacao.origem = %s', [id_usuario])

'''
Retorna uma lista de dicionários de usuários que seguem este usuário.
'''
@default_fetch_many
def get_seguidores_usuario_pk(id_usuario):
    return ('SELECT * FROM relacao INNER JOIN usuario ON usuario.id_usuario = relacao.origem WHERE relacao.tipo = 0 AND relacao.alvo = %s', [id_usuario])





'''
Retorna uma lista de dicionários de comentários da postagem.
'''
@default_fetch_many
def get_comentarios_postagem_pk(id_postagem):
    return ('SELECT * FROM opiniao INNER JOIN comentario ON opiniao.id_post = comentario.id_post WHERE comentario.id_postagem = %s', [id_postagem])



'''
Retorna uma lista de dicionários de opiniões que contém o tópico especificado.
'''
@default_fetch_many
def get_opinioes_topico_pk(nome_topico):
    return ('SELECT * FROM opiniao INNER JOIN citacao_topico ON opiniao.id_post = citacao_topico.id_post WHERE citacao_topico.nome_topico = %s ORDER BY opiniao.data_post DESC', [nome_topico])


'''
Retorna uma lista de dicionários de opiniões que contém o tópico especificado.
'''
@default_fetch_many
def get_usuarios_busca(substring):
    substring = "%" + substring + "%"
    return ('SELECT * FROM usuario WHERE nome_usuario ILIKE %s OR nome_real ILIKE %s OR biografia ILIKE %s ORDER BY cont_seguidores DESC', [substring, substring, substring])



















'''
-------------------------
INSERTS!
-------------------------
'''



'''
Magia negra: Faz uma operação no banco de dados e commita imediatamente.
'''
def default_commit_one(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        r = default_fetch_one(fn)(*args, **kwargs)
        commit_changes()
        return r
    return wrapped

'''
Magia negra: Faz uma operação no banco de dados e commita imediatamente.
'''
def default_commit_none(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        r = default_fetch_none(fn)(*args, **kwargs)
        commit_changes()
        return r
    return wrapped







'''
Insere um usuário no banco de dados.
Recebe um dicionário como parâmetro.
Retorna uma lista(?) contendo as chaves primárias.
'''
@default_commit_one
def inserir_usuario(u):
    return (("INSERT INTO usuario (nome_usuario, nome_real, biografia, senha, foto, visibilidade)"
            "VALUES (%(nome_usuario)s, %(nome_real)s, %(biografia)s, %(senha)s, %(foto)s, %(visibilidade)s) RETURNING id_usuario"), u)



'''
Insere uma postagem no banco de dados.
Recebe um dicionário como parâmetro.
Retorna uma lista(?) contendo as chaves primárias.
'''
@default_commit_one
def inserir_postagem(p):
    id_post = __impl_default_fetch((
        ("INSERT INTO opiniao (texto, foto, dono, data_post, comentario)"
        "VALUES (%(texto)s, %(foto)s, %(dono)s, %(data_post)s, FALSE) RETURNING id_post"), p))[0]
    p['id_post'] = id_post
    return ("INSERT INTO postagem (id_post) VALUES (%(id_post)s) RETURNING id_post", p)



'''
Insere um comentário no banco de dados.
Recebe um dicionário como parâmetro.
Retorna uma lista(?) contendo as chaves primárias.
'''
@default_commit_one
def inserir_comentario(p):
    id_post = __impl_default_fetch((
        ("INSERT INTO opiniao (texto, foto, dono, data_post, comentario)"
        "VALUES (%(texto)s, %(foto)s, %(dono)s, %(data_post)s, TRUE) RETURNING id_post"), p))[0]
    p['id_post'] = id_post
    return ("INSERT INTO comentario (id_post, id_postagem) VALUES (%(id_post)s, %(id_postagem)s) RETURNING id_post", p)



'''
Insere uma relação entre usuários no banco de dados.
Recebe um dicionário como parâmetro.
Retorna uma lista(?) contendo as chaves primárias.
'''
@default_commit_one
def inserir_relacao(u):
    return (("INSERT INTO relacao(tipo, origem, alvo)"
            "VALUES (%(tipo)s, %(origem)s, %(alvo)s) RETURNING origem, alvo"), u)



'''
Insere um tópico no banco de dados.
Recebe um dicionário como parâmetro.
Retorna uma lista(?) contendo as chaves primárias.
'''
@default_commit_one
def inserir_topico(t):
    return (("INSERT INTO topico(nome_topico)"
            "VALUES (%(nome_topico)s) RETURNING nome_topico"), t)



'''
Insere uma citação no banco de dados.
Recebe um dicionário como parâmetro.
Retorna uma lista(?) contendo as chaves primárias.
'''
@default_commit_one
def inserir_citacao(u):
    return (("INSERT INTO citacao_topico(id_post, nome_topico)"
            "VALUES (%(id_post)s, %(nome_topico)s) RETURNING id_citacao_topico"), u)



'''
Insere uma marcação no banco de dados.
Recebe um dicionário como parâmetro.
Retorna uma lista(?) contendo as chaves primárias.
'''
@default_commit_one
def inserir_marcacao(u):
    return (("INSERT INTO marcacoes(id_post, id_usuario)"
            "VALUES (%(id_post)s, %(id_usuario)s) RETURNING id_marcacoes"), u)



'''
Insere uma notificação no banco de dados.
Recebe um dicionário como parâmetro.
Retorna uma lista(?) contendo as chaves primárias.
'''
@default_commit_one
def inserir_notificacao(u):
    return (("INSERT INTO notificacao(tipo, lida, data_evento, dono_notificacao, mencionado, conteudo)"
            "VALUES (%(tipo)s, %(lida)s, %(data_evento)s, %(dono_notificacao)s, %(mencionado)s, %(conteudo)s) RETURNING id_notificacao"), u)














'''
-------------------------
UPDATES!
-------------------------
'''


def __update_dict_to_set(r, ex=[]):
    ex = ex if hasattr(ex, '__iter__') and not isinstance(ex, str) else [ex]
    return ', '.join(['{0} = %({0})s'.format(i) for i in dict(r) if not i in ex])



'''
Atualiza uma relação entre dois usuários.
Recebe um dicionário como parâmetro.
Consulte get_relacao_usuario_pk.
'''
@default_commit_none
def update_relacao_usuario(r):
    return ('UPDATE relacao SET tipo = %(tipo)s WHERE origem = %(origem)s AND alvo = %(alvo)s', r)


'''
Atualiza as informações de um usuário.
'''
@default_commit_none
def update_usuario(r):
    return ('UPDATE usuario SET ' + __update_dict_to_set(r, 'id_usuario') + ' WHERE id_usuario = %(id_usuario)s', r)


'''
Atualiza as informações de uma notificação.
'''
@default_commit_none
def update_notificacao(r):
    return ('UPDATE notificacao SET ' + __update_dict_to_set(r, 'id_notificacao') + ' WHERE id_notificacao = %(id_notificacao)s', r)










'''
-------------------------
TRASH!
-------------------------
'''







def clear_db():
    tables = ['citacao_topico', 'comentario', 'marcacoes', 'notificacao', 'opiniao', 'postagem', 'relacao', 'topico', 'usuario']
    for t in tables:
        get_db().execute('DROP TABLE IF EXISTS {} CASCADE'.format(t))
    get_db().execute(get_base_schema())
    commit_changes()


def btests_0():
    import datetime

    clear_db()
    vk = inserir_usuario({'nome_usuario': 'vk', 'nome_real': 'VK', 'biografia': 'Sysadmin dessa porra',
                          'senha': 'numsei', 'foto': 'também numsei', 'visibilidade': True})[0]
    teste = inserir_usuario({'nome_usuario': 'teste', 'nome_real': 'Teste', 'biografia': 'Useless profile',
                             'senha': 'numsei', 'foto': 'também numsei', 'visibilidade': False})[0]
    leandro = inserir_usuario({'nome_usuario': 'leandro', 'nome_real': 'Leandro', 'biografia': 'Useless dev',
                               'senha': 'numsei', 'foto': 'também numsei', 'visibilidade': True})[0]
    wilson = inserir_usuario({'nome_usuario': 'wilson', 'nome_real': 'Wilson', 'biografia': 'BFF ever',
                              'senha': 'numsei', 'foto': 'também numsei', 'visibilidade': True})[0]

    inserir_relacao({'tipo': 0, 'origem': vk, 'alvo': wilson})
    inserir_relacao({'tipo': 0, 'origem': vk, 'alvo': teste})
    inserir_relacao({'tipo': 0, 'origem': vk, 'alvo': leandro})
    inserir_relacao({'tipo': 0, 'origem': teste, 'alvo': leandro})
    inserir_relacao({'tipo': 0, 'origem': leandro, 'alvo': vk})

    terminar_top = inserir_topico({'nome_topico': 'terminar'})[0]

    inserir_postagem({'texto': "WIIILSOOOON!!!", 'foto': 'wilson.jpg', 'dono': vk, 'data_post': datetime.datetime.now()})
    terminar_post = inserir_postagem({'texto': "Bora #terminar isso logo. @leandro", 'foto': '*', 'dono': vk, 'data_post': datetime.datetime.now()})[0]

    inserir_marcacao({'id_post': terminar_post, 'id_usuario': leandro})
    inserir_citacao({'id_post': terminar_post, 'nome_topico': terminar_top})

    comentario = inserir_comentario({'texto': "Já vou", 'foto': '', 'dono': leandro, 'id_postagem': terminar_post, 'data_post': datetime.datetime.now()})[0]
    inserir_citacao({'id_post': comentario, 'nome_topico': terminar_top})

    inserir_notificacao({'tipo': 0, 'lida': False, 'data_evento': datetime.datetime.now(),
                         'dono_notificacao': vk, 'mencionado': wilson, 'conteudo': None})
    inserir_notificacao({'tipo': 0, 'lida': False, 'data_evento': datetime.datetime.now(),
                         'dono_notificacao': wilson, 'mencionado': vk, 'conteudo': None})
    inserir_notificacao({'tipo': 1, 'lida': True, 'data_evento': datetime.datetime.now(),
                         'dono_notificacao': leandro, 'mencionado': None, 'conteudo': terminar_post})



