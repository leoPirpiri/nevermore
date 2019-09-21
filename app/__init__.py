from flask import Flask
from .initdb import init_app

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app

app = create_app()
from app.controllers import routers