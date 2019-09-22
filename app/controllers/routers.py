from flask import render_template, g
from app import app
from app.auth import login_required, logout_required
from app.models.post import get_timeline

from app.controllers.opinions import _opinar

@app.route("/index/")
@app.route("/")
@logout_required
def index():
    return render_template("index.html")

@app.route("/home/")
@login_required
def home():
    return render_template("home.html", posts=get_timeline(g.user))

@app.route("/perfil/")
@login_required
def perfil():
    return render_template("perfil.html")

@app.route("/post/")
@login_required
def post():
    return render_template("perfil.html")

@app.route("/opinar", methods=("GET", "POST"))
@login_required
def opinar():
    """Permite ao usuário emitir uma opinião"""
    return _opinar()