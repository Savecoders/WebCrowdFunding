from oracledb import Connection, Cursor
from src.models import Proyecto
from src.schema import GruposColaboradoresDao


class ProyectoDao:
    def __init__(self, conn: Connection, cursor: Cursor) -> None:
        self.__conn = conn
        self.__cursor = cursor

    def insert(self, proyecto: Proyecto) -> None:
        if proyecto is None:
            raise ValueError("The Error al insertar el proyecto")

        sql = """
        INSERT INTO PROYECTOS (IDPROYECTO, NOMBRE, IDEA, DESCRIPCION, FECHALIMITE, PRESENTACION, PRESUPUESTO, RECOMPENSA, METAALCANZADA, ESTADO, IDGRUPO)
        VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)
        """

        self.__cursor.execute(sql, proyecto.inserdao())
        self.__conn.commit()

    def get_all_proyects(self) -> list[Proyecto]:
        self.__cursor.execute("SELECT * FROM PROYECTOS")
        data = self.__cursor.fetchall()

        proyectos = []

        for row in data:

            # get group

            grupo = GruposColaboradoresDao(self.__conn, self.__cursor)
            grupo = grupo.get_by_id(row[10])

            if grupo is None:
                raise ValueError("The group doesn't exists.")

            proyecto = Proyecto(row[0], row[1], row[2], row[3],
                                row[4], row[5], row[6], row[7],
                                row[8], row[9]
                                )

            proyecto.group = grupo

            proyectos.append(proyecto)

        return proyectos

    def get_by_id(self, id) -> Proyecto:
        sql = """
        SELECT * FROM PROYECTOS
        WHERE IDPROYECTO = :1
        """
        values = (id,)
        self.__cursor.execute(sql, values)
        data = self.__cursor.fetchone()

        if data is None:
            return None

        # get group

        grupo = GruposColaboradoresDao(self.__conn, self.__cursor)
        grupo = grupo.get_by_id(data[10])

        if grupo is None:
            raise ValueError("The group doesn't exists.")

        print(data)

        proyecto = Proyecto(data[0], data[1], data[2], data[3],
                            data[4], data[5], data[6], data[7],
                            data[8], data[9]
                            )

        proyecto.load_image()

        proyecto.group = grupo

        return proyecto

    def get_by_name(self, nombre: str) -> Proyecto:
        sql = """
        SELECT * FROM PROYECTOS
        WHERE NOMBRE = :1
        """
        values = (nombre,)
        self.__cursor.execute(sql, values)
        data = self.__cursor.fetchone()

        if data is None:
            return None

        # get group

        grupo = GruposColaboradoresDao(self.__conn, self.__cursor)
        grupo = grupo.get_by_id(data[10])

        if grupo is None:
            raise ValueError("The group doesn't exists.")

        proyecto = Proyecto(data[0], data[1], data[2], data[3],
                            data[4], data[5], data[6], data[7],
                            data[8], data[9]
                            )

        proyecto.group = grupo

        return proyecto

    def check_name(self, nombre) -> bool:
        sql = """
        SELECT * FROM PROYECTOS
        WHERE NOMBRE = :1
        """
        values = (nombre,)
        self.__cursor.execute(sql, values)
        data = self.__cursor.fetchone()

        if data is None:
            return False

        return True

    def update_all_info(self, proyecto: Proyecto):
        sql = """
        UPDATE PROYECTOS
        SET IDEA = :1, NOMBRE = :2, FECHALIMITE = :3, PRESENTACION = :4, PRESUPUESTO = :5, RECOMPENSA = :6, ESTADO = :7
        """
        values = (proyecto.idea, proyecto.nombre, proyecto.fechaLimite, proyecto.get_binary_presentacion(), proyecto.presupuesto, proyecto.recompensa,
                  proyecto.metaAlcanzada, proyecto.estado)
        self.__cursor.execute(sql, values)
        self.__conn.commit()

    def get_projects_by_group(self, id) -> list[Proyecto]:

        sql = """
        SELECT * FROM PROYECTOS
        WHERE IDGRUPO = :1
        """
        values = (id,)
        self.__cursor.execute(sql, values)
        data = self.__cursor.fetchall()

        proyectos = []

        for row in data:

            proyecto = Proyecto()

            proyecto.idProyecto = row[0]

            proyecto.nombre = row[1]

            proyecto.idea = row[2]

            proyecto.fechaLimite = row[4]

            proyecto.insert_binary_image(row[5])

            proyecto.presupuesto = row[6]

            proyecto.load_image()

            proyectos.append(proyecto)

        return proyectos

    def update_basic_info(self, proyecto: Proyecto):
        sql = """
        UPDATE PROYECTOS
        SET IDEA = :1, NOMBRE = :2, FECHALIMITE = :3, PRESENTACION = :4, RECOMPENSA = :5, 
        """
        values = (proyecto.idea, proyecto.nombre, proyecto.fechaLimite, proyecto.get_binary_presentacion(), proyecto.recompensa,
                  proyecto.metaAlcanzada)
        self.__cursor.execute(sql, values)
        self.__conn.commit()

    def delete(self, id):

        # check if user includes in a group

        sqlCheck = """
        SELECT * FROM PROYECTOS
        WHERE IDPROYECTO = :1
        """

        valuesCheck = (id,)

        self.__cursor.execute(sqlCheck, valuesCheck)
        data = self.__cursor.fetchone()

        if data is not None:
            raise ValueError(
                "Sorry the user includes in a group and can't be deleted")

        # delete user

        sql = """
        DELETE FROM PROYECTOS
        WHERE IDPROYECTO = :1
        """
        values = (id,)
        self.__cursor.execute(sql, values)
        self.__conn.commit()
