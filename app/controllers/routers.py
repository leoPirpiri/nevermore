from flask import g, request, redirect, url_for, send_from_directory, render_template as rendert, jsonify
from app import app

from app.auth import login_required, logout_required, usuario_logado
from app.models.post import get_timeline
from app.models.opinion import buscar_opinioes_por_topico
from app.models.notification import get_notificacoes_usuario
from app.models import user

from app.controllers.opinions import _opinar, _obter_foto
from app.models import opinion

from app.controllers.dateToDate import formatDate

from functools import wraps

def render_template(*args, **kwargs):
    if usuario_logado():
        return rendert(logged_user = g.user, notificacoes = get_notificacoes_usuario(g.user), *args, **kwargs)
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
                            opinar_form=True,
                            assuntos = opinion.buscar_trend_topics()
                            )


@app.route("/busca/")
@login_required
def busca():
    if request.method == "GET":
        termo = request.args.get("termo", None)
        if termo is None or len(termo) == 0:
            return redirect(url_for('index'))
        elif termo[0] == '#':
            return render_template("home.html", posts=buscar_opinioes_por_topico(termo[1:]), termo=termo, assuntos = opinion.buscar_trend_topics())
        else:
            return render_template("usuarios.html", usuarios=user.buscar_usuarios_por_string(termo), termo=termo)
    return redirect(url_for('index'))

@app.route("/perfil/")
@login_required
def perfil():
    return render_template("perfil.html",
                           posts=g.user.get_postagens(),
                           opinar_form=True,
                           assuntos = opinion.buscar_trend_topics()
                        )


@app.route("/post/")
@login_required
def post():
    return render_template("perfil.html")


@app.route("/opinar", methods=("GET", "POST"))
@login_required
def opinar():
    """Permite ao usuário emitir uma opinião"""
    return _opinar()


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
def json_c():
    retorno = _opinar()
    retorno['data_post'] = formatDate(retorno['data_post'])
    return jsonify(retorno)


@app.route("/foto_perfil/<nome_usuario>")
def foto_perfil(nome_usuario, id_usuario=None):
    if not nome_usuario is None:
        u = user.get_user(nome_usuario)
    elif not id_usuario is None:
        u = user.User(id_usuario)
    else:
        u = None

    from os import path
    basedir = app.config['IMAGES_USERS_ABS']
    vpath = path.join(basedir, u.foto())
    if not u is None and u.e_valido() and u.foto() and path.exists(vpath):
        return send_from_directory(basedir, u.foto())

    return send_from_directory(app.static_folder, 'images_app/default-user.png')
