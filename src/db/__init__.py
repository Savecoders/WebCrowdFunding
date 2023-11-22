import oracledb
import click

from flask import current_app as app, g
from flask.cli import with_appcontext

from src.schema.schemas import instructions


class DataBase:
    def __init__(self) -> None:
        self.connection = oracledb.connect(
            port=app.config['DATABASE_PORT'],
            user=app.config['DATABASE_USER'],
            password=app.config['DATABASE_PASSWORD'],
            dsn=app.config['DATABASE_DSN'],
            host=app.config['DATABASE_HOST']
        )
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def initialize(self) -> None:
        for i in instructions:
            self.cursor.execute(i)
        self.connection.commit()

    # cursor
    @property
    def cursor(self) -> oracledb.Cursor:
        return self.cursor

    def openCursor(self) -> None:
        self.cursor = self.connection.cursor()

    def closeCursor(self) -> None:
        self.cursor.close()

    # querys for database

    # single query
    def query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()

    #################
    # * into query
    #################

    # --------------------------
    # Table "USUARIOS"
    # --------------------------

    # ---------SQL SYNTAX----------------
    # CREATE TABLE USUARIOS (
    #  IDUSUARIO NUMBER PRIMARY KEY,
    #  NOMBRES VARCHAR2(50 CHAR) NOT NULL,
    #  CONTRASENA VARCHAR2(255 CHAR) NOT NULL,
    #  TELEFONO VARCHAR2(15 CHAR) NOT NULL,
    #  ESTADO VARCHAR2(20 CHAR) NOT NULL,
    #  EMAIL VARCHAR2(100 CHAR) UNIQUE,
    #  IMAGENPERFIL VARCHAR2(50 CHAR),
    #  PAIS VARCHAR2(100 CHAR) NOT NULL,
    #  CIUDAD VARCHAR2(100 CHAR) NOT NULL,
    #  FECHANACIMIENTO DATE
    # );
    # ---------------------------------

    # INTO QUERY
    def insert_user(self, id, nombres, contrasena, telefono,
                    estado, email, image_perfil, pais, ciudad, fecha_nacimiento):
        self.cursor.execute(
            f"""
            INSERT INTO USUARIOS (IDUSUARIO, NOMBRES, CONTRASENA, TELEFONO, ESTADO, EMAIL, IMAGENPERFIL, PAIS, CIUDAD, FECHANACIMIENTO)
            VALUES ('{id}', '{nombres}', '{contrasena}', '{telefono}', '{estado}', '{email}', '{image_perfil}', '{pais}', '{ciudad}', '{fecha_nacimiento}')
            """
        )
        self.connection.commit()

    # SELECT QUERY

    # SELECT ALL USERS
    def get_users(self):
        self.cursor.execute(
            f"""
            SELECT * FROM USUARIOS
            """
        )
        return self.cursor.fetchall()

    # SELECT USER BY ID
    def get_user_by_id(self, id):
        self.cursor.execute(
            f"""
            SELECT * FROM USUARIOS
            WHERE IDUSUARIO = '{id}'
            """
        )
        return self.cursor.fetchone()

    # UPDATE QUERY

    # UPDATE ALL INFO
    def update_user_allinfo(self, id, nombres, contrasena, telefono,
                            estado, email, image_perfil, pais, ciudad, fecha_nacimiento):
        self.cursor.execute(
            f"""
            UPDATE USUARIOS
            SET NOMBRES = '{nombres}', CONTRASENA = '{contrasena}', TELEFONO = '{telefono}', ESTADO = '{estado}', EMAIL = '{email}', IMAGENPERFIL = '{image_perfil}', PAIS = '{pais}', CIUDAD = '{ciudad}', FECHANACIMIENTO = '{fecha_nacimiento}'
            WHERE IDUSUARIO = '{id}'
            """
        )
        self.connection.commit()

    # UPDATE BASIC INFO
    def update_user_basicinfo(self, id, nombres, telefono, email, image_perfil, pais, ciudad, fecha_nacimiento):

        self.cursor.execute(
            f"""
            UPDATE USUARIOS
            SET NOMBRES = '{nombres}', TELEFONO = '{telefono}', EMAIL = '{email}', IMAGENPERFIL = '{image_perfil}', PAIS = '{pais}', CIUDAD = '{ciudad}', FECHANACIMIENTO = '{fecha_nacimiento}'
            WHERE IDUSUARIO = '{id}'
            """
        )

    # DELETE QUERY | WHERE IDUSUARIO = '{id}'
    def delete_user(self, id):
        self.cursor.execute(
            f"""
            DELETE FROM USUARIOS
            WHERE IDUSUARIO = '{id}'
            """
        )
        self.connection.commit()

    # --------------------------
    # Table "GRUPOSCOLABORADORES"
    # --------------------------

    # ---------SQL SYNTAX--------
    # CREATE TABLE GRUPOSCOLABORADORES (
    #   IDGRUPO NUMBER PRIMARY KEY,
    #   NOMBREGRUPO VARCHAR2(50 CHAR)
    # );
    # --------------------------
    # * Relation Table "USUARIOSGRUPOS"
    # * GRUPOSCOLABORADORES - USUARIOS
    # ---------SQL SYNTAX--------
    # CREATE TABLE USUARIOSGRUPOS (
    #   IDUSUARIO NUMBER,
    #   IDGRUPO NUMBER,
    #   PRIMARY KEY (IDUSUARIO, IDGRUPO)
    # );
    # --------------------------

    # INTO QUERY

    # INSERT GROUP QUERY
    def insert_group(self, id, nombre):
        self.cursor.execute(
            f"""
            INSERT INTO GRUPOSCOLABORADORES (IDGRUPO, NOMBREGRUPO)
            VALUES ('{id}', '{nombre}')
            """
        )
        self.connection.commit()

    # SELECT QUERY | WHERE IDGRUPO = '{id}'
    def get_group_by_id(self, id):
        self.cursor.execute(
            f"""
            SELECT * FROM GRUPOSCOLABORADORES
            WHERE IDGRUPO = '{id}'
            """
        )
        return self.cursor.fetchone()

    # UPDATE QUERY | WHERE IDGRUPO = '{id}'
    def update_group(self, id, nombre):
        self.cursor.execute(
            f"""
            UPDATE GRUPOSCOLABORADORES
            SET NOMBREGRUPO = '{nombre}'
            WHERE IDGRUPO = '{id}'
            """
        )
        self.connection.commit()

    # DELETE QUERY | WHERE IDGRUPO = '{id}'
    def delete_group(self, id):
        self.cursor.execute(
            f"""
            DELETE FROM GRUPOSCOLABORADORES
            WHERE IDGRUPO = '{id}'
            """
        )
        self.connection.commit()

    # INSERT USER-GROUP QUERY
    def insert_user_group(self, id_usuario, id_grupo):
        self.cursor.execute(
            f"""
            INSERT INTO USUARIOSGRUPOS (IDUSUARIO, IDGRUPO)
            VALUES ('{id_usuario}', '{id_grupo}')
            """
        )
        self.connection.commit()

    # SELECT ALL USERS-GROUPS
    def get_users_groups(self):
        self.cursor.execute(
            f"""
            SELECT U.IDUSUARIO, G.IDGRUPO
            FROM USUARIOS U, GRUPOSCOLABORADORES G, USUARIOSGRUPOS UG
            WHERE U.IDUSUARIO = UG.IDUSUARIO AND G.IDGRUPO = UG.IDGRUPO
            """
        )
        return self.cursor.fetchall()

    # SELECT ALL USERS-NAMES-GROUPS
    def get_users_names_groups(self):
        self.cursor.execute(
            f"""
            SELECT U.IDUSUARIO, U.NOMBRES, G.IDGRUPO, G.NOMBREGRUPO
            FROM USUARIOS U, GRUPOSCOLABORADORES G, USUARIOSGRUPOS UG
            WHERE U.IDUSUARIO = UG.IDUSUARIO AND G.IDGRUPO = UG.IDGRUPO
            """
        )
        return self.cursor.fetchall()

    # REMOVE USER FROM GROUP
    def remove_user_from_group(self, id_usuario, id_grupo):
        self.cursor.execute(
            f"""
            DELETE FROM USUARIOSGRUPOS
            WHERE IDUSUARIO = '{id_usuario}' AND IDGRUPO = '{id_grupo}'
            """
        )
        self.connection.commit()

    # --------------------------
    # Table "PROYECTOS"
    # --------------------------


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
