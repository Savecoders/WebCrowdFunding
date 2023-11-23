from oracledb import Connection, Cursor


class GruposColaboradoresDao:

    def __init__(self, conn: Connection, cursor: Cursor) -> None:
        self.__conn = conn
        self.__cursor = cursor

    # --------------------------
    # ? Table "GRUPOSCOLABORADORES"
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

    # INSERT GROUP QUERY

    def insert(self, id, nombre):
        self.cursor.execute(
            f"""
            INSERT INTO GRUPOSCOLABORADORES (IDGRUPO, NOMBREGRUPO)
            VALUES ('{id}', '{nombre}')
            """
        )
        self.__conn.commit()

    # SELECT QUERY | WHERE IDGRUPO = '{id}'
    def get_by_id(self, id):
        self.__cursor.execute(
            f"""
            SELECT * FROM GRUPOSCOLABORADORES
            WHERE IDGRUPO = '{id}'
            """
        )
        return self.__cursor.fetchone()

    # UPDATE QUERY | WHERE IDGRUPO = '{id}'
    def update(self, id, nombre):
        self.__cursor.execute(
            f"""
            UPDATE GRUPOSCOLABORADORES
            SET NOMBREGRUPO = '{nombre}'
            WHERE IDGRUPO = '{id}'
            """
        )
        self.__conn.commit()

    # DELETE QUERY | WHERE IDGRUPO = '{id}'
    def delete(self, id):
        self.__cursor.execute(
            f"""
            DELETE FROM GRUPOSCOLABORADORES
            WHERE IDGRUPO = '{id}'
            """
        )
        self.__conn.commit()

    # INSERT USER-GROUP QUERY
    def insert_user(self, id_usuario, id_grupo):
        self.__cursor.execute(
            f"""
            INSERT INTO USUARIOSGRUPOS (IDUSUARIO, IDGRUPO)
            VALUES ('{id_usuario}', '{id_grupo}')
            """
        )
        self.__conn.commit()

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

    # SELECT ALL USERS-NAMES-GROUPS
    def get_users_names(self):
        self.__cursor.execute(
            f"""
            SELECT U.IDUSUARIO, U.NOMBRES, G.IDGRUPO, G.NOMBREGRUPO
            FROM USUARIOS U, GRUPOSCOLABORADORES G, USUARIOSGRUPOS UG
            WHERE U.IDUSUARIO = UG.IDUSUARIO AND G.IDGRUPO = UG.IDGRUPO
            """
        )
        return self.__cursor.fetchall()

    # REMOVE USER FROM GROUP
    def remove_user(self, id_usuario, id_grupo):
        self.__cursor.execute(
            f"""
            DELETE FROM USUARIOSGRUPOS
            WHERE IDUSUARIO = '{id_usuario}' AND IDGRUPO = '{id_grupo}'
            """
        )
        self.__conn.commit()
