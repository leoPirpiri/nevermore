from flask import render_template
from app import app
from app.auth import login_required, logout_required
from app.controllers import trends

@app.route("/index/")
@app.route("/")
@logout_required
def index():
    return render_template("index.html")

@app.route("/home/")
@login_required
def home():
    return render_template("home.html")

@app.route("/perfil/")
@login_required
def perfil():
    return render_template("perfil.html", assuntos = trends.get_assuntos([]))