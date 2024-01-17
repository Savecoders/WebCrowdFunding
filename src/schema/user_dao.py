from src.models.user import Usuario


class UsuarioDao:

    def __init__(self, conn, cursor) -> None:
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

        # check if the user is valid

        if usuario is None:
            raise ValueError("The Error al insertar el usuario")

        # valid if the user already exists | email

        if self.check_email(usuario.email):
            raise ValueError("The email already exists")

        # | nombres/username
        if self.check_username(usuario.nombre):
            raise ValueError("The username already exists")

        sql = """
        INSERT INTO USUARIOS (IDUSUARIO, NOMBRES, CONTRASENA, TELEFONO, ESTADO, EMAIL, IMAGENPERFIL, PAIS, CIUDAD, FECHANACIMIENTO)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.__cursor.execute(sql, usuario.inserdao())
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
        WHERE IDUSUARIO = %s
        """
        values = (id,)
        self.__cursor.execute(sql, values)
        data = self.__cursor.fetchone()

        if data is None:
            return None

        usuario = Usuario(data[0], data[1], data[2], data[3],
                          data[4], data[5], data[6], data[7],
                          data[8], data[9]
                          )
        return usuario

    # SELECT USER BY EMAIL
    def get_by_email(self, email) -> Usuario:
        sql = """
        SELECT * FROM USUARIOS
        WHERE EMAIL = %s
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

    # CHECK IF EMAIL EXISTS

    def check_email(self, email) -> bool:
        sql = """
        SELECT * FROM USUARIOS
        WHERE EMAIL = %s
        """
        values = (email,)
        self.__cursor.execute(sql, values)
        data = self.__cursor.fetchone()

        if data is None:
            return False

        return True

    # CHECK IF USERNAME EXISTS

    def check_username(self, username) -> bool:
        sql = """
        SELECT * FROM USUARIOS
        WHERE NOMBRES = %s
        """
        values = (username,)
        self.__cursor.execute(sql, values)
        data = self.__cursor.fetchone()

        if data is None:
            return False

        return True

    # SELECT USER BY USERNAME
    def get_by_username(self, username) -> Usuario:
        sql = """
        SELECT * FROM USUARIOS
        WHERE NOMBRES = %s
        """
        values = (username,)
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
        SET NOMBRES = %s, CONTRASENA = %s, TELEFONO = %s, ESTADO = %s, EMAIL = %s, IMAGENPERFIL = %s, PAIS = %s, CIUDAD = %s, FECHANACIMIENTO = %s
        WHERE IDUSUARIO = %s
        """
        values = (usuario.nombre, usuario.contrasena, usuario.telefono, usuario.estado, usuario.email,
                  usuario.get_binary_image_perfil(), usuario.pais, usuario.ciudad, usuario.fecha_nacimiento, usuario.id_usuario)
        self.__cursor.execute(sql, values)
        self.__conn.commit()

    # UPDATE BASIC INFO
    def update_basic_info(self,  usuario: Usuario):
        sql = """
        UPDATE USUARIOS
        SET NOMBRES = %s, TELEFONO = %s, EMAIL = %s, IMAGENPERFIL = %s, PAIS = %s, CIUDAD = %s, FECHANACIMIENTO = %s
        WHERE IDUSUARIO = %s
        """
        values = (usuario.nombre, usuario.telefono, usuario.email, usuario.get_binary_image_perfil(),
                  usuario.pais, usuario.ciudad, usuario.fecha_nacimiento, usuario.id_usuario)
        self.__cursor.execute(sql, values)
        self.__conn.commit()

    # DELETE QUERY | WHERE IDUSUARIO = '{id}'
    def delete(self, id):

        # check if user includes in a group

        sqlCheck = """
        SELECT * FROM USUARIOSGRUPOS
        WHERE IDUSUARIO = %s
        """

        valuesCheck = (id,)

        self.__cursor.execute(sqlCheck, valuesCheck)
        data = self.__cursor.fetchone()

        if data is not None:
            raise ValueError(
                "Sorry the user includes in a group and can't be deleted")

        # delete user

        sql = """
        DELETE FROM USUARIOS
        WHERE IDUSUARIO = %s
        """
        values = (id,)
        self.__cursor.execute(sql, values)
        self.__conn.commit()
