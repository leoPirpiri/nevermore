from flask import Flask
from .initdb import init_app
from os import path

def create_app():
    app = Flask(__name__)
    rpath = path.abspath(path.join(app.root_path, '../'))
    app.config.from_mapping(
        IMAGES_USERS = 'IMAGES_USERS'
    )
    app.config.from_pyfile(path.join(rpath, 'app.cfg'))
    app.config.from_mapping(
        IMAGES_USERS_ABS = path.join(app.static_folder, app.config['IMAGES_USERS'])
    )
    init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app

app = create_app()
from app.controllers import routers