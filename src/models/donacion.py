import re
# uuid: Universally Unique Identifier
import hashlib
import uuid


class Donacion:

    def __init__(self, id_donacion=None, monto=None, fecha_donacion=None, id_usuario=None, id_proyecto=None) -> None:
        self.__id_donacion = id_donacion
        self.__monto = monto
        self.__fecha_donacion = fecha_donacion
        self.__id_usuario = id_usuario
        self.__id_proyecto = id_proyecto

    @property
    def id_donacion(self):
        return self.__id_donacion

    @id_donacion.setter
    def id_donacion(self, id_donacion):
        self.__id_donacion = id_donacion

    @property
    def monto(self):
        return self.__monto

    @monto.setter
    def monto(self, monto):

        if str(monto).isdigit() == False:
            raise ValueError("El monto debe ser un número")

        if float(monto) > 0:
            self.__monto = float(monto)
        else:
            raise ValueError("El monto no puede ser menor o igual a 0")

    @property
    def fecha_donacion(self):
        return self.__fecha_donacion

    @fecha_donacion.setter
    def fecha_donacion(self, fecha_donacion):

        if fecha_donacion == "":
            raise ValueError("La fecha no puede estar vacía")

        self.__fecha_donacion = fecha_donacion

    @property
    def id_usuario(self):
        return self.__id_usuario

    @id_usuario.setter
    def id_usuario(self, id_usuario):
        self.__id_usuario = id_usuario

    @property
    def id_proyecto(self):
        return self.__id_proyecto

    @id_proyecto.setter
    def id_proyecto(self, id_proyecto):
        self.__id_proyecto = id_proyecto

    def generateHashId(self):
        self.__id_donacion = hashlib.sha256(uuid.uuid4().bytes).hexdigest()

    def inserdao(self):
        return (self.__id_donacion, self.__monto, self.__fecha_donacion, self.__id_usuario, self.__id_proyecto)
