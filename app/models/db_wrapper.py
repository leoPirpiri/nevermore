'''
Este módulo contém os SQLs e funções usuais de acesso ao BD.
'''

from flask import g


'''
Retorna um dicionário para uma instância de usuário.
'''
def get_usuario_pk(id_usuario):
    return {}


'''
Retorna um dicionário para uma instância de Postagem.
'''
def get_postagem_pk(id_post):
    return {}


'''
Retorna um dicionário para uma instância de Comentário.
'''
def get_comentario_pk(id_post):
    return {}




'''
Retorna uma lista de dicionários de notificações do usuário.
'''
def get_notificacoes_usuario_pk(id_usuario):
    return []

'''
Retorna uma lista de dicionários de postagens do usuário.
'''
def get_postagens_usuario_pk(id_usuario):
    return []

'''
Retorna uma lista de dicionários de usuários que este usuário segue.
'''
def get_seguindo_usuario_pk(id_usuario):
    return []

'''
Retorna uma lista de dicionários de usuários que seguem este usuário.
'''
def get_seguidores_usuario_pk(id_usuario):
    return []

'''
Retorna uma lista de dicionários de usuários que este usuário bloqueou.
'''
def get_bloqueados_usuario_pk(id_usuario):
    return []




'''
Retorna uma lista de dicionários de comentários da postagem.
'''
def get_comentarios_postagem_pk(id_post):
    return []