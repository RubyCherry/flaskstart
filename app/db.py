import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def close_db(e=None):
    db = g.pop('db', None)
    
    print("close_db", type(g), db)
    if db is not None:
        db.close()


def get_db():
    if 'db' not in g:
        
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Чистит БД и создает новые таблицы"""
    init_db()
    click.echo('БД создана')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)