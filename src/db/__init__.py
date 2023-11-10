
import oracledb
import click

from flask import current_app as app, g
from flask.cli import with_appcontext

from src.schema.schemas import instructions


class Database:
    pass


def get_db():
    if 'db' not in g:
        g.db = oracledb.connect(
            port=app.config['DATABASE_PORT'],
            user=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASSWORD'],
            dsn=app.config['DATABASE_DSN'],
            host=app.config['DATABASE_HOST']
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c


def close_db(e=None):
    db = g.pop('db', None)

    # db no is None/Void, close db
    if db is not None:
        db.close()


def init_db():
    db, c = get_db()

    for i in instructions:
        c.execute(i)

    db.commit()


@click.command('init-db')
# access from envioment vars
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Database initialization complete')


def init_app(app):
    # execute functions to finally app
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
