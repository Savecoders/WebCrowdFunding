
from oracledb import Connection, Cursor
from src.models.user import Usuario


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
    def insert(self, usuario: Usuario) -> None:

        sql = """
        INSERT INTO USUARIOS (IDUSUARIO, NOMBRES, CONTRASENA, TELEFONO, ESTADO, EMAIL, IMAGENPERFIL, PAIS, CIUDAD, FECHANACIMIENTO)
        VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)
        """
        values = (usuario.id_usuario, usuario.nombres, usuario.contrasena,
                  usuario.telefono, usuario.estado,
                  usuario.email, usuario.get_binary_image_perfil(), usuario.pais,
                  usuario.ciudad, usuario.fecha_nacimiento)
        self.__cursor.execute(sql, values)
        self.__conn.commit()

    # SELECT QUERY

    # SELECT ALL USERS

    def get_all_users(self) -> list[Usuario]:
        self.__cursor.execute("SELECT * FROM USUARIOS")
        data = self.__cursor.fetchall()

        usuarios = []

        for row in data:
            usuario = Usuario(row[0], row[1], row[2], row[3],
                              row[4], row[5], row[6], row[7],
                              row[8], row[9]
                              )

            usuarios.append(usuario)

        return usuarios

    # SELECT USER BY ID

    def get_by_id(self, id) -> Usuario:
        sql = """
        SELECT * FROM USUARIOS
        WHERE IDUSUARIO = :1
        """
        values = (id,)
        self.__cursor.execute(sql, values)
        data = self.__cursor.fetchone()

        usuario = Usuario(data[0], data[1], data[2], data[3],
                          data[4], data[5], data[6], data[7],
                          data[8], data[9]
                          )
        return usuario

    # SELECT USER BY EMAIL
    def get_by_email(self, email) -> Usuario:
        sql = """
        SELECT * FROM USUARIOS
        WHERE EMAIL = :1
        """
        values = (email,)
        self.__cursor.execute(sql, values)
        data = self.__cursor.fetchone()

        if data is None:
            return None

        usuario = Usuario(data[0], data[1], data[2], data[3],
                          data[4], data[5], data[6], data[7],
                          data[8], data[9]
                          )

        return usuario

    # UPDATE QUERY

    # UPDATE ALL INFO

    def update_all_info(self, usuario: Usuario):
        sql = """
        UPDATE USUARIOS
        SET NOMBRES = :1, CONTRASENA = :2, TELEFONO = :3, ESTADO = :4, EMAIL = :5, IMAGENPERFIL = :6, PAIS = :7, CIUDAD = :8, FECHANACIMIENTO = :9
        WHERE IDUSUARIO = :10
        """
        values = (usuario.nombres, usuario.contrasena, usuario.telefono, usuario.estado, usuario.email,
                  usuario.get_binary_image_perfil(), usuario.pais, usuario.ciudad, usuario.fecha_nacimiento, usuario.id)
        self.__cursor.execute(sql, values)
        self.__conn.commit()

    # UPDATE BASIC INFO
    def update_basic_info(self,  usuario: Usuario):
        sql = """
        UPDATE USUARIOS
        SET NOMBRES = :1, TELEFONO = :2, EMAIL = :3, IMAGENPERFIL = :4, PAIS = :5, CIUDAD = :6, FECHANACIMIENTO = :7
        WHERE IDUSUARIO = :8
        """
        values = (usuario.nombres, usuario.telefono, usuario.email, usuario.get_binary_image_perfil(),
                  usuario.pais, usuario.ciudad, usuario.fecha_nacimiento, usuario.id)
        self.__cursor.execute(sql, values)
        self.__conn.commit()

    # DELETE QUERY | WHERE IDUSUARIO = '{id}'
    def delete(self, id):
        sql = """
        DELETE FROM USUARIOS
        WHERE IDUSUARIO = :1
        """
        values = (id,)
        self.__cursor.execute(sql, values)
        self.__conn.commit()
