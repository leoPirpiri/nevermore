import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext
from .models.db_wrapper import get_db, close_cur


def init_db():
    db = get_db()
    pass # DO SOMETHING

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_cur)
    app.cli.add_command(init_db_command)
