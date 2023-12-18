from oracledb import Connection, Cursor
from src.models import Donacion


class DonacionDao:

    def __init__(self, conn: Connection, cursor: Cursor) -> None:
        self.__conn = conn
        self.__cursor = cursor

    def insert(self, donacion: Donacion) -> None:

        if donacion is None:
            raise ValueError("The Error al insertar la donacion")

        sql = """
        INSERT INTO DONACION (IDDONACION, MONTO, FECHADONACION, IDUSUARIO, IDPROYECTO)
        VALUES (:1, :2, :3, :4, :5)
        """

        self.__cursor.execute(sql, donacion.inserdao())
        self.__conn.commit()

        sql = """
        INSERT INTO PROYECTOS_DONACION (IDPROYECTO, IDDONACION)
        VALUES (:1, :2)
        """

        values = (donacion.id_proyecto, donacion.id_donacion)

        self.__cursor.execute(sql, values)

        self.__conn.commit()

    def get_all_donations_by_user(self, id_user: str) -> list[Donacion]:

        sql = """
        SELECT * FROM DONACION WHERE IDUSUARIO = :1
        """

        self.__cursor.execute(sql, (id_user,))

        data = self.__cursor.fetchall()

        if not data:
            return None

        donaciones = []

        for row in data:

            donacion = Donacion(row[0], row[1], row[2], row[3], row[4])

            donaciones.append(donacion)

        return donaciones

    def get_all_donations_by_project(self, id_project: str) -> list[Donacion]:

        sql = """
        SELECT * FROM DONACION WHERE IDPROYECTO = :1
        """

        self.__cursor.execute(sql, (id_project,))

        data = self.__cursor.fetchall()

        if not data:
            return None

        donaciones = []

        for row in data:

            donacion = Donacion(row[0], row[1], row[2], row[3], row[4])

            donaciones.append(donacion)

        return donaciones

    def get_all_donations(self) -> list[Donacion]:

        sql = """
        SELECT * FROM DONACION
        """

        self.__cursor.execute(sql)

        data = self.__cursor.fetchall()

        if not data:
            return None

        donaciones = []

        for row in data:

            donacion = Donacion(row[0], row[1], row[2], row[3], row[4])

            donaciones.append(donacion)

        return donaciones
