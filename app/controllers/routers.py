from flask import render_template, g, request, redirect, url_for
from app import app
from app.auth import login_required, logout_required

from app.models.post import get_timeline
from app.models.opinion import buscar_opinioes_por_topico
from app.models.notification import get_notificacoes_usuario
from app.models.user import buscar_usuarios_por_string

from app.controllers.opinions import _opinar
from app.models import opinion


@app.route("/index/")
@app.route("/")
@logout_required
def index():
    return render_template("index.html")

@app.route("/home/")
@login_required
def home():
    return render_template("home.html", logged_user = g.user, posts=get_timeline(g.user), opinar_form=True, assuntos = opinion.buscar_trend_topics(), notificacoes = get_notificacoes_usuario(g.user))


@app.route("/busca/")
@login_required
def busca():
    if request.method == "GET":
        termo = request.args.get("termo", None)
        if termo is None or len(termo) == 0:
            return redirect(url_for('index'))
        elif termo[0] == '#':
            return render_template("home.html", logged_user = g.user, posts=buscar_opinioes_por_topico(termo[1:]), opinar_form=False, notificacoes = get_notificacoes_usuario(g.user), termo=termo, assuntos = opinion.buscar_trend_topics())
        else:
            return render_template("usuarios.html", usuarios=buscar_usuarios_por_string(termo), notificacoes = get_notificacoes_usuario(g.user), termo=termo)
    return redirect(url_for('index'))

@app.route("/perfil/")
@login_required
def perfil():
    return render_template("perfil.html", logged_user = g.user, posts=g.user.get_postagens(), assuntos = opinion.buscar_trend_topics())

@app.route("/post/")
@login_required
def post():
    return render_template("perfil.html")

@app.route("/opinar", methods=("GET", "POST"))
@login_required
def opinar():
    """Permite ao usuário emitir uma opinião"""
    return _opinar()
 
