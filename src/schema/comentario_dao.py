import psycopg2
from src.models import Comentario, Usuario

from src.schema import UsuarioDao


class ComentarioDao:

    def __init__(self, conn, cursor) -> None:
        self.__conn = conn
        self.__cursor = cursor

    # --------------------------
    # ? Table "COMENTARIOS"
    # --------------------------
    # IDCOMENTARIO VARCHAR2(255 CHAR) PRIMARY KEY,
    # COMENTARIO VARCHAR2(400 CHAR),
    # FECHACOMENTARIO DATE,
    # IDUSUARIO VARCHAR2(255 CHAR),
    # IDPROYECTO VARCHAR2(255 CHAR)

    # INTO QUERY

    # INSERT COMMENT QUERY

    def insert(self, comentario: Comentario):

        sql = """
            INSERT INTO COMENTARIOS (IDCOMENTARIO, COMENTARIO, FECHACOMENTARIO, IDUSUARIO, IDPROYECTO)
            VALUES (%s, %s, %s, %s, %s)
            """

        values = (comentario.id_comentario, comentario.comentario,
                  comentario.fecha_comentario, comentario.usuario.id_usuario, comentario.id_proyecto)

        self.__cursor.execute(sql, values)
        self.__conn.commit()

    # GET ALL COMMENTS IN A PROJECT

    def get_all_comments_by_project(self, id_proyecto: str) -> list[Comentario]:

        sql = """
            SELECT * FROM COMENTARIOS WHERE IDPROYECTO = %s
            """

        self.__cursor.execute(sql, (id_proyecto,))

        comments_dao = self.__cursor.fetchall()

        if not comments_dao:
            return None

        comments = []

        for comment in comments_dao:

            # get user by id

            usuario = UsuarioDao(self.__conn, self.__cursor).get_by_id(
                comment[3])

            usuario.load_image_perfil()

            comentario = Comentario(
                comment[0], comment[1], comment[2], usuario, comment[4])

            comments.append(comentario)

        return comments
