from flask import render_template
from app import app

@app.route("/index/")
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home/")
def home():
    return render_template("home.html")

@app.route("/perfil/")
def perfil():
    return render_template("perfil.html")