from oracledb import Connection, Cursor 
from src.models.proyecto import Proyecto
class ProyectoDao:
    def __init__(self, conn: Connection, cursor: Cursor) -> None:
        self.__conn = conn
        self.__cursor = cursor
    def insert(self, proyecto: Proyecto) -> None:
        if proyecto is None:
            raise ValueError("The Error al insertar el proyecto")
        
        sql = """
        INSERT INTO PROYECTO (IDPROYECTO, IDEA, NOMBRE, FECHALIMITE, PRESENTACION, PRESUPUESTO, RECOMPENSA, METAALCANZADA, ESTADO, IDGRUPO,IDDONACION)
        VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11 )
        """
        
        self.__cursor.execute(sql, proyecto.inserdao)
        self.__conn.commit()
        values = (proyecto.idProyecto, proyecto.idea, proyecto.nombre,
                  proyecto.fechaLimite, proyecto.get_binary_presentacion(),
                  proyecto.presupuesto, proyecto.recompensa, proyecto.metaAlcanzada,
                  proyecto.estado)
    def get_all_proyects(self) -> list[Proyecto]:
        self.__cursor.execute("SELECT * FROM PROYECTOS")
        data = self.__cursor.fetchall()

        proyectos = []

        for row in data:
            proyecto = Proyecto(row[0], row[1], row[2], row[3],
                              row[4], row[5], row[6], row[7],
                              row[8], row[9], row[10]
                              )

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

        proyecto = Proyecto(data[0], data[1], data[2], data[3],
                          data[4], data[5], data[6], data[7],
                          data[8], data[9], data[10]
                          )
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

        proyecto = Proyecto(data[0], data[1], data[2], data[3],
                          data[4], data[5], data[6], data[7],
                          data[8], data[9],  data[10]
                          )

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
                 proyecto.metaAlcanzada , proyecto.estado)
        self.__cursor.execute(sql, values)
        self.__conn.commit()

    def update_basic_info(self, proyecto: Proyecto):
        sql = """
        UPDATE PROYECTOS
        SET IDEA = :1, NOMBRE = :2, FECHALIMITE = :3, PRESENTACION = :4, RECOMPENSA = :5, 
        """
        values = (proyecto.idea, proyecto.nombre, proyecto.fechaLimite, proyecto.get_binary_presentacion(), proyecto.recompensa,
                 proyecto.metaAlcanzada )
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
