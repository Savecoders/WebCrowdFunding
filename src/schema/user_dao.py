
from oracledb import Connection, Cursor


class UsuarioDao:

    def __init__(self, conn: Connection, cursor: Cursor) -> None:
        self.__conn = conn
        self.__cursor = cursor

    # --------------------------
    # ? Table "USUARIOS"
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
    def insert(self, id, nombres, contrasena, telefono,
               estado, email, image_perfil, pais, ciudad, fecha_nacimiento):
        self.__cursor.execute(
            f"""
            INSERT INTO USUARIOS (IDUSUARIO, NOMBRES, CONTRASENA, TELEFONO, ESTADO, EMAIL, IMAGENPERFIL, PAIS, CIUDAD, FECHANACIMIENTO)
            VALUES ('{id}', '{nombres}', '{contrasena}', '{telefono}', '{estado}', '{email}', '{image_perfil}', '{pais}', '{ciudad}', '{fecha_nacimiento}')
            """
        )
        self.__conn.commit()

    # SELECT QUERY

    # SELECT ALL USERS
    def get_all_users(self):
        self.__cursor.execute(
            f"""
            SELECT * FROM USUARIOS
            """
        )
        return self.__cursor.fetchall()

    # SELECT USER BY ID
    def get_by_id(self, id):
        self.__cursor.execute(
            f"""
            SELECT * FROM USUARIOS
            WHERE IDUSUARIO = '{id}'
            """
        )
        return self.__cursor.fetchone()

    # UPDATE QUERY

    # UPDATE ALL INFO
    def update_all_info(self, id, nombres, contrasena, telefono,
                        estado, email, image_perfil, pais, ciudad, fecha_nacimiento):
        self.__cursor.execute(
            f"""
            UPDATE USUARIOS
            SET NOMBRES = '{nombres}', CONTRASENA = '{contrasena}', TELEFONO = '{telefono}', ESTADO = '{estado}', EMAIL = '{email}', IMAGENPERFIL = '{image_perfil}', PAIS = '{pais}', CIUDAD = '{ciudad}', FECHANACIMIENTO = '{fecha_nacimiento}'
            WHERE IDUSUARIO = '{id}'
            """
        )
        self.__conn.commit()

    # UPDATE BASIC INFO
    def update_basic_info(self, id, nombres, telefono, email, image_perfil, pais, ciudad, fecha_nacimiento):

        self.__cursor.execute(
            f"""
            UPDATE USUARIOS
            SET NOMBRES = '{nombres}', TELEFONO = '{telefono}', EMAIL = '{email}', IMAGENPERFIL = '{image_perfil}', PAIS = '{pais}', CIUDAD = '{ciudad}', FECHANACIMIENTO = '{fecha_nacimiento}'
            WHERE IDUSUARIO = '{id}'
            """
        )

    # DELETE QUERY | WHERE IDUSUARIO = '{id}'
    def delete(self, id):
        self.__cursor.execute(
            f"""
            DELETE FROM USUARIOS
            WHERE IDUSUARIO = '{id}'
            """
        )
        self.__conn.commit()
