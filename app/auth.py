import functools


from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.models import user as users
from app.initdb import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("index"))
        return view(*args, **kwargs)
    return wrapped_view


def logout_required(view):
    """View decorator that redirects authenticated users to the home page."""
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if not g.user is None:
            return redirect(url_for("home"))
        return view(*args, **kwargs)
    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = users.User(user_id)


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        fullname = request.form.get("input_signup_name", None)
        username = request.form.get("input_signup_user", None)
        password = request.form.get("input_signup_senha", None)
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif not users.get_user(username) is None:
            error = "User {0} is already registered.".format(username)

        if error is None:
            u=users.registrar_usuario({'nome_usuario': username, 'nome_real': fullname, 'senha': password, 'visibilidade': True})
            session["user_id"] = u.id_usuario()
            return redirect(url_for("home"))

        flash(error)

    return redirect(url_for("index"))


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form.get("input_login_user", None)
        password = request.form.get("input_login_senha", "")
        db = get_db()
        error = None
        user = users.get_user(username)

        if user is None:
            error = "Incorrect username."
        elif user.senha() != password:
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = user.id_usuario()
            return redirect(url_for("home"))

        flash(error)

    return redirect(url_for("index"))


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))



