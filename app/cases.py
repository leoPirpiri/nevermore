from app.models.db_wrapper import clear_db
from app.models import user, post, comment, notification

from datetime import timedelta
from datetime import datetime as dt

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

    dtn = dt.now()
    datenow = dtn - timedelta(seconds=2)
    post.criar_post("TO BE DELETED!!!", "nooo.jpg", vk, data=datenow, topicos=['delete'])
    datenow = dtn - timedelta(seconds=1)
    post.criar_post("WIIILSOOOON!!!", "wilson.jpg", vk, data=datenow, topicos=['bff'])
    p = post.criar_post("Bora #terminar isso logo. @leandro", "", vk, marcados=[leandro], topicos=['terminar'])

    comment.criar_comentario("Já vou", "", leandro, p, marcados=[teste, vk], topicos=['terminar'])


    notification.criar_notificacao_post(leandro, p)
    notification.criar_notificacao_usuario(vk, teste, notification.NotificationType.ACEITA_SOLICITACAO)
    n = notification.criar_notificacao_usuario(vk, wilson, notification.NotificationType.NOVO_SEGUIDOR)
    n.marcar_lida()



def usercase_1():
    usercase_0()

    vk = user.User(nome_usuario='vk')
    leandro = user.User(nome_usuario='leandro')
    assert vk.get_relacionamento(leandro) == user.Relacionamento.SEGUINDO
    ps = vk.get_postagens()
    assert len(ps) == 3
    ps[2].excluir()
    assert ps[1].texto() == "WIIILSOOOON!!!"
    assert "terminar" in ps[0].texto()
    c = ps[0].get_comentarios()
    assert len(c) == 1
    assert "vou" in c[0].texto()
    assert 1 == sum(1 if i.lida() else 0 for i in notification.get_notificacoes_usuario(vk))

usercase_1()