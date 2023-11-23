import oracledb
import click

from flask import current_app as app, g
from flask.cli import with_appcontext

# schemas dao
from src.schema import (instructions, UsuarioDao,
                        GruposColaboradoresDao, ComentarioDao,
                        DonacionDao, ProyectoDao)

# models dto
from src.models import (Usuarios, GruposColaboradores,
                        Proyecto, Donacion, Comentario)


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
        self.__usuario_dao = UsuarioDao(self.connection, self.cursor)
        self.__grupos_colaboradores_dao = GruposColaboradoresDao(
            self.connection, self.cursor)

    def __del__(self):
        self.connection.close()

    # initialize database
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
    # ? Table "USUARIOS"
    # --------------------------

    # INTO QUERY
    def insert_user(self, usuario: Usuarios):
        self.__usuario_dao.insert(usuario.id, usuario.nombres, usuario.contrasena,
                                  usuario.telefono, usuario.estado, usuario.email,
                                  usuario.image_perfil, usuario.pais,
                                  usuario.ciudad, usuario.fecha_nacimiento
                                  )

    # SELECT QUERY

    # SELECT ALL USERS

    def get_users(self):
        return self.__usuario_dao.get_all_users()
    # SELECT USER BY ID

    def get_user_by_id(self, id):
        return self.__usuario_dao.get_by_id(id)

    # UPDATE QUERY

    # UPDATE ALL INFO
    def update_user_allinfo(self, usuario: Usuarios):
        self.__usuario_dao.update_all_info(usuario.id, usuario.nombres, usuario.contrasena,
                                           usuario.telefono, usuario.estado,
                                           usuario.email, usuario.image_perfil,
                                           usuario.pais, usuario.ciudad, usuario.fecha_nacimiento
                                           )

    # UPDATE BASIC INFO
    def update_user_basicinfo(self, usuario: Usuarios):
        self.__usuario_dao.update_basic_info(usuario.id, usuario.nombres, usuario.telefono,
                                             usuario.email, usuario.image_perfil, usuario.pais,
                                             usuario.ciudad, usuario.fecha_nacimiento)

    # DELETE QUERY | WHERE IDUSUARIO = '{id}'
    def delete_user(self, id):
        self.__usuario_dao.delete(id)

    # --------------------------
    # ? Table "GRUPOSCOLABORADORES"
    # --------------------------

    # INTO QUERY

    # INSERT GROUP QUERY
    def insert_group(self, grupo: GruposColaboradores):
        self.__grupos_colaboradores_dao.insert(
            id, grupo.id_grupo_colaboradores, grupo.nombre)

    # SELECT QUERY | WHERE IDGRUPO = '{id}'
    def get_group_by_id(self, id):
        return self.__grupos_colaboradores_dao.get_by_id(id)

    # UPDATE QUERY | WHERE IDGRUPO = '{id}'
    def update_group(self,  grupo: GruposColaboradores):
        self.__grupos_colaboradores_dao.update(
            grupo.id_grupo_colaboradores, grupo.nombre)

    # DELETE QUERY | WHERE IDGRUPO = '{id}'
    def delete_group(self, id):
        self.__grupos_colaboradores_dao.delete(id)

    # INSERT USER-GROUP QUERY
    def insert_user_group(self, id_usuario, id_grupo):
        self.__grupos_colaboradores_dao.insert_user(id_usuario, id_grupo)

    # SELECT ALL USERS-GROUPS
    def get_users_groups(self):
        return self.__grupos_colaboradores_dao.get_users()

    # SELECT ALL USERS-NAMES-GROUPS
    def get_users_names_groups(self):
        return self.__grupos_colaboradores_dao.get_users_names()

    # REMOVE USER FROM GROUP
    def remove_user_from_group(self, id_usuario, id_grupo):
        self.__grupos_colaboradores_dao.remove_user(id_usuario, id_grupo)

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


def init_app(app: app):
    # execute functions to finally app
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
