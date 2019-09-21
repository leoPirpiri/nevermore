from app.models.db_wrapper import clear_db
from app.models import user, post, comment, notification


def usercase_0():
    clear_db()

    vk = user.registrar_usuario({'nome_usuario': 'vk', 'nome_real': 'VK', 'biografia': 'Sysadmin dessa porra',
                          'senha': 'numsei', 'foto': 'também numsei', 'visibilidade': True})
    teste = user.registrar_usuario({'nome_usuario': 'teste', 'nome_real': 'Teste', 'biografia': 'Useless profile',
                             'senha': 'numsei', 'foto': 'também numsei', 'visibilidade': False})
    leandro = user.registrar_usuario({'nome_usuario': 'leandro', 'nome_real': 'Leandro', 'biografia': 'Useless dev',
                               'senha': 'numsei', 'foto': 'também numsei', 'visibilidade': True})
    wilson = user.registrar_usuario({'nome_usuario': 'wilson', 'nome_real': 'Wilson', 'biografia': 'BFF ever',
                              'senha': 'numsei', 'foto': 'também numsei', 'visibilidade': True})
    
    vk.set_relacionamento(wilson, user.Relacionamento.SEGUINDO)
    vk.set_relacionamento(teste, user.Relacionamento.SEGUINDO)
    vk.set_relacionamento(leandro, user.Relacionamento.SEGUINDO)
    teste.set_relacionamento(leandro, user.Relacionamento.SEGUINDO)
    leandro.set_relacionamento(vk, user.Relacionamento.SEGUINDO)

    leandro.set_relacionamento(wilson, user.Relacionamento.BLOQUEADO)


    post.criar_post("WIIILSOOOON!!!", "wilson.jpg", vk, topicos=['bff'])
    p = post.criar_post("Bora #terminar isso logo. @leandro", "", vk, marcados=[leandro], topicos=['terminar'])

    comment.criar_comentario("Já vou", "", leandro, p, marcados=[teste, vk], topicos=['terminar'])


    notification.criar_notificacao_post(leandro, p)
    notification.criar_notificacao_usuario(vk, teste, notification.NotificationType.ACEITA_SOLICITACAO)
    notification.criar_notificacao_usuario(vk, wilson, notification.NotificationType.NOVO_SEGUIDOR)



usercase_0()