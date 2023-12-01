import oracledb
import click

from flask import current_app as app, g
from flask.cli import with_appcontext


# in this class we have all functions to connect with database
# but you don't need to use this class, you can use the functions

class DataBase:
    def __init__(self) -> None:
        self._connection = oracledb.connect(
            port=app.config['DATABASE_PORT'],
            user=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASSWORD'],
            dsn=app.config['DATABASE_DSN'],
            host=app.config['DATABASE_HOST']
        )
        self._cursor = self._connection.cursor()

    # initialize database
    def initialize(self) -> None:
        # path: src/db/tables.sql
        with open('tables.sql', 'r') as file:
            sql_commands = file.read().split(';')
            for command in sql_commands:
                if command.strip() != '':
                    self._cursor.execute(command)
        self._connection.commit()

    # cursor get and setter
    @property
    def cursor(self) -> oracledb.Cursor:
        return self._cursor

    @cursor.setter
    def cursor(self, cursor: oracledb.Cursor) -> None:
        self._cursor = cursor

    @property
    def connection(self) -> oracledb.Connection:
        return self._connection

    @connection.setter
    def connection(self, connection: oracledb.Connection) -> None:
        self._connection = connection

    def openCursor(self) -> None:
        self._cursor = self._connection.cursor()

    def closeCursor(self) -> None:
        self._cursor.close()

    # close connection
    def close(self) -> None:
        self._connection.close()

    # querys for database

    # single query
    def query(self, query):
        self._cursor.execute(query)
        return self._cursor.fetchone()

# ----------------------
#!   Functions of db app
# ----------------------


def get_db():
    if 'db' not in g:
        g.db = oracledb.connect(
            port=app.config['DATABASE_PORT'],
            user=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASSWORD'],
            dsn=app.config['DATABASE_DSN'],
            host=app.config['DATABASE_HOST']
        )
        g.c = g.db.cursor()
    return g.db, g.c


def close_db(e=None):
    db = g.pop('db', None)

    # db no is None/Void, close db
    if db is not None:
        db.close()


def init_db():
    db, c = get_db()

    # path: src/db/tables.sql
    with open('src/db/tables.sql', 'r') as file:
        sql_commands = file.read().split(';')
        for command in sql_commands:
            if command.strip() != '':
                c.execute(command)

    c.connection.commit()

    db.commit()


@click.command('init-db')
# access from envioment vars
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Database initialization complete')


def init_app(app: app):
    # execute functions to finally app
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
