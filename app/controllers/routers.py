from flask import render_template, g, request, redirect, url_for
from app import app
from app.auth import login_required, logout_required

from app.models.post import get_timeline
from app.models.opinion import buscar_opinioes_por_topico

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
    return render_template("home.html", logged_user = g.user, posts=get_timeline(g.user), opinar_form=True, assuntos = opinion.buscar_trend_topics())

@app.route("/topico/")
@login_required
def busca_topico():
    if request.method == "GET":
        topico = request.args.get("topico", None)
        if not topico is None:
            return render_template("home.html", logged_user = g.user, posts=buscar_opinioes_por_topico(topico), opinar_form=False, assuntos = opinion.buscar_trend_topics())
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
 
