from flask import g, request, redirect, url_for, send_from_directory, render_template as rendert, jsonify, abort
from app import app

from app.auth import login_required, logout_required, usuario_logado
from app.models.post import get_timeline, Post
from app.models.opinion import buscar_opinioes_por_topico
from app.models import notification
from app.models import user

from app.controllers.opinions import _opinar, _obter_foto
from app.models import opinion

from app.controllers.dateToDate import formatDate

from functools import wraps

def render_template(*args, **kwargs):
    if usuario_logado():
        default_kwargs = {
            "logged_user": g.user,
            "notificacoes": ('proxy', notification.get_notificacoes_usuario, [g.user], {}),
            "assuntos": ('proxy', opinion.buscar_trend_topics),
            "formatDate": formatDate
        }
        default_kwargs.update(kwargs)
        for k, v in default_kwargs.items():
            if isinstance(v, tuple) and v[0] == 'proxy':
                if len(v) == 4:
                    default_kwargs[k] = v[1](*v[2], **v[3])
                else:
                    default_kwargs[k] = v[1]()
        return rendert(*args, **default_kwargs)
    else:
        return rendert(*args, **kwargs)

@app.route("/index/")
@app.route("/")
@logout_required
def index():
    return render_template("index.html")

@app.route("/home/")
@login_required
def home():
    return render_template("home.html",
                            posts=get_timeline(g.user),
                            opinar_form=True
                            )


@app.route("/busca/")
@login_required
def busca():
    if request.method == "GET":
        termo = request.args.get("termo", None)
        if termo is None or len(termo) == 0:
            return redirect(url_for('index'))
        elif termo[0] == '#':
            def topost(p):
                r = p.get_postagem() if p.comentario() else p
                return r.id_post(), r
            d = dict(topost(p) for p in buscar_opinioes_por_topico(termo[1:]))
            return render_template("home.html", posts=d.values(), termo=termo)
        else:
            return render_template("usuarios.html", usuarios=user.buscar_usuarios_por_string(termo), termo=termo)
    return redirect(url_for('index'))

@app.route("/perfil/")
@login_required
def perfil():
    return render_template("perfil.html",
                           posts=g.user.get_postagens(),
                           opinar_form=True,
                           num_seguindo = len(g.user.get_seguindo()),
                           num_seguidores = len(g.user.get_seguidores())
                        )

@app.route("/usuario/<nome_usuario>")
@login_required
def usuario(nome_usuario):
    if not nome_usuario is None:
        u = user.get_user(nome_usuario)
    else:
        u = None
    
    if u is None or not u.e_valido():
        return abort(404)
    
    return render_template("perfil_outros.html",
                           posts=u.get_postagens(),
                           outro = u,
                           num_seguindo = len(u.get_seguindo()),
                           num_seguidores = len(u.get_seguidores())
                        )

@app.route("/comunidade/")
@login_required
def comunidade():
    return render_template("comunidade.html", seguidores = g.user.get_seguidores(), seguindo = g.user.get_seguindo(),
     bloqueados=g.user.get_bloqueados())


@app.route("/post/<id_post>")
@login_required
def post(id_post):
    p = Post(id_post)
    if not p.e_valido():
        abort(404)
    elif p.comentario():
        return redirect(url_for('post', id_post=p.get_postagem().id_post()))
    return render_template("home.html", posts=[p])


@app.route("/opinar", methods=("GET", "POST"))
@login_required
def opinar():
    """Permite ao usuário emitir uma opinião"""
    p = _opinar()
    return redirect(url_for('post', id_post=p.id_post()))


@app.route("/foto_perfil_atualizar", methods=("GET", "POST"))
@login_required
def foto_perfil_atualizar():
    """Permite ao usuário atualizar a foto de perfil"""
    if request.method == "POST":
        foto = _obter_foto()
        if not foto is None:
            g.user.atualizar_dados_usuario({'foto': foto})
            return "SUCESS"
    return "INVALID OPERATION"
 

@app.route("/comentar", methods=("GET", "POST"))
@login_required
def json_adiciona_comentario():
    retorno = _opinar().to_dict()
    retorno['data_post'] = formatDate(retorno['data_post'])
    return jsonify(retorno)

@app.route("/desopinar", methods=("GET", "POST"))
@login_required
def json_remove_post():
    p=Post(request.form.get("post", None))
    p.excluir()
    retorno = {'ret': 'ALGUMACOISA'}
    #retorno['data_post'] = formatDate(retorno['data_post'])
    return jsonify(retorno)

@app.route("/descomentar", methods=("GET", "POST"))
@login_required
def json_remove_coment():
    p=Post(request.form.get("post", None))
    p.excluir()
    retorno = {'ret': 'ALGUMACOISA'}
    #retorno['data_post'] = formatDate(retorno['data_post'])
    return jsonify(retorno)

@app.route("/atualizarbio", methods=("GET", "POST"))
@login_required
def json_atualizar_biografia():
    bio = request.form.get("biografia", None)
    g.user.atualizar_dados_usuario({'biografia': bio})
    retorno = {'ret': 'ALGUMACOISA'}
    #retorno['data_post'] = formatDate(retorno['data_post'])
    return jsonify(retorno)


@app.route("/foto_perfil/<nome_usuario>")
@login_required
def foto_perfil(nome_usuario, id_usuario=None):
    if not nome_usuario is None:
        u = user.get_user(nome_usuario)
    elif not id_usuario is None:
        u = user.User(id_usuario)
    else:
        u = None

    from os import path
    basedir = app.config['IMAGES_USERS_ABS']
    if not u is None and u.e_valido() and u.foto() and path.exists(path.join(basedir, u.foto())):
        return send_from_directory(basedir, u.foto())

    return send_from_directory(app.static_folder, 'images_app/default-user.png')





@app.route("/de_seguir/<nome_usuario>")
@login_required
def de_seguir(nome_usuario, id_usuario=None):
    if not nome_usuario is None:
        u = user.get_user(nome_usuario)
    elif not id_usuario is None:
        u = user.User(id_usuario)
    else:
        u = None
    
    if u is None or not u.e_valido():
        return abort(404)
    
    rel = g.user.get_relacionamento(u)
    if rel is user.Relacionamento.NONE:
        u.solicitar_seguir(g.user)
    elif rel is user.Relacionamento.SEGUINDO or rel is user.Relacionamento.SOLICITOU:
        u._set_relacionamento(g.user, user.Relacionamento.NONE)
    
    return redirect(url_for('usuario', nome_usuario=nome_usuario))


@app.route("/aceitar/<nome_usuario>")
@login_required
def aceitar(nome_usuario, id_usuario=None):
    if not nome_usuario is None:
        u = user.get_user(nome_usuario)
    elif not id_usuario is None:
        u = user.User(id_usuario)
    else:
        u = None
    
    if u is None or not u.e_valido():
        return abort(404)
    
    user.aceitar_solicitacao(u, g.user)
    return redirect(url_for('usuario', nome_usuario=nome_usuario))


@app.route("/de_bloquear/<nome_usuario>")
@login_required
def de_bloquear(nome_usuario, id_usuario=None):
    if not nome_usuario is None:
        u = user.get_user(nome_usuario)
    elif not id_usuario is None:
        u = user.User(id_usuario)
    else:
        u = None
    
    if u is None or not u.e_valido():
        return abort(404)
    
    rel = g.user.get_relacionamento(u)
    if rel is user.Relacionamento.BLOQUEOU:
        u.desbloquear(g.user)
        return redirect(url_for('usuario', nome_usuario=nome_usuario))
    else:
        u.bloquear(g.user)
    
    return redirect(url_for('index'))


@app.route("/marcarlida/", methods=("GET", "POST"))
@login_required
def marcarlida():
    for n in notification.get_notificacoes_usuario(g.user):
        n.marcar_lida()
    return ""
