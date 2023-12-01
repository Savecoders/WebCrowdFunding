from oracledb import Connection, Cursor

# user model

from src.models import GruposColaboradores, Usuario, UsuarioGrupo


class GruposColaboradoresDao:

    def __init__(self, conn: Connection, cursor: Cursor) -> None:
        self.__conn = conn
        self.__cursor = cursor

    # --------------------------
    # ? Table "GRUPOSCOLABORADORES"
    # --------------------------

    # ---------SQL SYNTAX--------
    # CREATE TABLE GRUPOSCOLABORADORES (
    #   IDGRUPO VARCHAR2(255 CHAR) PRIMARY KEY,
    #   NOMBREGRUPO VARCHAR2(80 CHAR),
    #   DESCRIPCION VARCHAR2(120 CHAR),
    #   IMAGEN BLOB,
    #   FECHACREACION VARCHAR2(120 CHAR),
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

    # INSERT GROUP QUERY

    def insert(self, grupo: GruposColaboradores):

        # grupo exists ?

        if self.get_by_id(grupo.id_grupo_colaboradores):
            raise ValueError("The group already exists.")

        # name in use ?

        if self.get_by_name(grupo.nombre):
            raise ValueError("The name is already in use.")

        sql = """
        INSERT INTO GRUPOSCOLABORADORES (IDGRUPO, NOMBREGRUPO, DESCRIPCION, IMAGEN, FECHACREACION)
        VALUES (:1, :2, :3, :4, :5)
        """

        values = (grupo.id_grupo_colaboradores, grupo.nombre, grupo.descripcion,
                  grupo.get_binary_image(), grupo.fecha_creacion)

        self.__cursor.execute(sql, values)

        self.__conn.commit()

    # SELECT QUERY | WHERE IDGRUPO = '{id}'
    def get_by_id(self, id):

        sql = "SELECT * FROM GRUPOSCOLABORADORES WHERE IDGRUPO = :1"

        values = (id,)

        self.__cursor.execute(sql, values)

        # object Grupos Colaboradores

        row = self.__cursor.fetchone()

        if row:
            grupo = GruposColaboradores(row[0], row[1], row[2], row[3], row[4])
            return grupo
        else:
            return None

    # SELECT QUERY | WHERE NOMBREGRUPO = '{nombre}'

    def get_by_name(self, nombre):

        sql = "SELECT * FROM GRUPOSCOLABORADORES WHERE NOMBREGRUPO = :1"

        values = (nombre,)

        self.__cursor.execute(sql, values)

        # object Grupos Colaboradores

        grupo = GruposColaboradores()

        row = self.__cursor.fetchone()

        if row:
            grupo.id_grupo_colaboradores = row[0]
            grupo.nombre = row[1]
            grupo.descripcion = row[2]
            grupo.imagen = row[3]
            grupo.fecha_creacion = row[4]

            return grupo
        else:
            return None

    # UPDATE QUERY | WHERE IDGRUPO = '{id}'

    def update(self, grupo: GruposColaboradores):

        sql = "UPDATE GRUPOSCOLABORADORES SET NOMBREGRUPO = :1, DESCRIPCION = :2, IMAGEN = :3, FECHACREACION = :4 WHERE IDGRUPO = :5"

        values = (grupo.nombre, grupo.descripcion, grupo.imagen,
                  grupo.fecha_creacion, grupo.id_grupo_colaboradores)

        self.__cursor.execute(sql, values)

        self.__conn.commit()

    # DELETE QUERY | WHERE IDGRUPO = '{id}'
    def delete(self, id):
        sql = "DELETE FROM GRUPOSCOLABORADORES WHERE IDGRUPO = :1"

        values = (id,)

        self.__cursor.execute(sql, values)

        self.__conn.commit()

    # INSERT USER-GROUP QUERY
    def insert_user(self, id_usuario, id_grupo):

        # user in group ?

        if self.check_user_in_group(id_usuario, id_grupo):
            raise ValueError("The user is already in the group.")

        sql = "INSERT INTO USUARIOSGRUPOS (IDUSUARIO, IDGRUPO) VALUES (:1, :2)"

        values = (id_usuario, id_grupo)

        self.__cursor.execute(sql, values)
        self.__conn.commit()

    # SELECT QUERY
    def get_groups(self, id_usuario):
        sql = """
        SELECT G.IDGRUPO, G.NOMBREGRUPO, G.DESCRIPCION, G.IMAGEN, G.FECHACREACION
        FROM GRUPOSCOLABORADORES G, USUARIOSGRUPOS UG
        WHERE G.IDGRUPO = UG.IDGRUPO AND UG.IDUSUARIO = :1
        """
        values = (id_usuario,)
        self.__cursor.execute(sql, values)

        data = self.__cursor.fetchall()

        if data is None:
            return None

        grupos = []

        for row in data:
            grupo = GruposColaboradores(row[0], row[1], row[2], row[3], row[4])
            # get users by group

            usuarios = self.get_users_by_group(grupo.id_grupo_colaboradores)

            grupo.usuario_grupos = usuarios
            grupos.append(grupo)

        return grupos

    # SELECT ALL USERS-GROUPS

    def get_users(self):
        self.__cursor.execute(
            f"""
            SELECT U.IDUSUARIO, G.IDGRUPO
            FROM USUARIOS U, GRUPOSCOLABORADORES G, USUARIOSGRUPOS UG
            WHERE U.IDUSUARIO = UG.IDUSUARIO AND G.IDGRUPO = UG.IDGRUPO
            """
        )
        return self.__cursor.fetchall()

    # SELECT ALL USERS by IDGRUPO
    def get_users_by_group(self, id_grupo) -> list[Usuario]:

        sql = """
                SELECT U.IDUSUARIO, U.NOMBRES, U.EMAIL, U.IMAGENPERFIL, G.IDGRUPO, G.NOMBREGRUPO
                FROM USUARIOS U, GRUPOSCOLABORADORES G, USUARIOSGRUPOS UG
                WHERE U.IDUSUARIO = UG.IDUSUARIO AND G.IDGRUPO = UG.IDGRUPO AND G.IDGRUPO = :1
            """
        values = (id_grupo,)

        self.__cursor.execute(sql, values)

        data = self.__cursor.fetchall()

        if data is None:
            return None

        usuarios = []

        for row in data:
            usuario = Usuario()

            usuario.id_usuario = row[0]
            usuario.nombre = row[1]
            usuario.email = row[2]
            usuario.insert_binary_image(row[3])

            # usuario image_perfil

            usuario.load_image_perfil()

            usuarios.append(usuario)

        return usuarios

    # SELECT ALL USERS-NAMES-GROUPS
    def get_users_names(self):
        sql = """
        SELECT U.IDUSUARIO, U.NOMBRES, G.IDGRUPO, G.NOMBREGRUPO
        FROM USUARIOS U, GRUPOSCOLABORADORES G, USUARIOSGRUPOS UG
        WHERE U.IDUSUARIO = UG.IDUSUARIO AND G.IDGRUPO = UG.IDGRUPO
        """
        self.__cursor.execute(sql)
        return self.__cursor.fetchall()

    # SELECT ALL usernames by IDGRUPO

    def get_usernames_by_group(self, id_grupo):
        sql = """
        SELECT U.NOMBRES
        FROM USUARIOS U, GRUPOSCOLABORADORES G, USUARIOSGRUPOS UG
        WHERE U.IDUSUARIO = UG.IDUSUARIO AND G.IDGRUPO = UG.IDGRUPO AND G.IDGRUPO = :1
        """
        values = (id_grupo,)
        self.__cursor.execute(sql, values)
        return [row[0] for row in self.__cursor.fetchall()]

    # REMOVE USER FROM GROUP
    def remove_user(self, id_usuario, id_grupo):
        self.__cursor.execute(
            f"""
            DELETE FROM USUARIOSGRUPOS
            WHERE IDUSUARIO = '{id_usuario}' AND IDGRUPO = '{id_grupo}'
            """
        )
        self.__conn.commit()

    # CHECK USER IN GROUP

    def check_user_in_group(self, id_usuario, id_grupo):

        sql = """
        SELECT * FROM USUARIOSGRUPOS
        WHERE IDUSUARIO = :1 AND IDGRUPO = :2
        """
        values = (id_usuario, id_grupo)

        self.__cursor.execute(sql, values)

        data = self.__cursor.fetchone()

        if data is None:
            return False
        else:
            return True

    def load_grupo_colaboradores(self, id_grupo):
        grupo = self.get_by_id(id_grupo)
        usuarios = self.get_users_by_group(id_grupo)

        for usuario in usuarios:
            usuario_grupo = UsuarioGrupo(usuario, grupo)
            grupo.add_usuario_grupo(usuario_grupo)

        return grupo
