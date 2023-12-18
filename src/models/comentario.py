
import re
# uuid: Universally Unique Identifier
import hashlib
import uuid


class Comentario:
    def __init__(self, id_comentario=None, comentario=None, fecha_comentario=None, usuario=None, id_proyecto=None) -> None:
        self.__id_comentario = id_comentario
        self.__comentario = comentario
        self.__fecha_comentario = fecha_comentario
        self.__usuario = usuario
        self.__id_proyecto = id_proyecto

    @property
    def id_comentario(self):
        return self.__id_comentario

    @id_comentario.setter
    def id_comentario(self, id_comentario):
        self.__id_comentario = id_comentario

    @property
    def comentario(self):
        return self.__comentario

    @comentario.setter
    def comentario(self, comentario):
        if comentario == "":
            raise ValueError("El comentario no puede estar vacío")

        if len(comentario) > 400:
            raise ValueError(
                "El comentario no puede exceder los 400 caracteres")

        self.__comentario = comentario

    @property
    def fecha_comentario(self):
        return self.__fecha_comentario

    @fecha_comentario.setter
    def fecha_comentario(self, fecha_comentario):

        if fecha_comentario == "":
            raise ValueError("La fecha no puede estar vacía")

        self.__fecha_comentario = fecha_comentario

    @property
    def usuario(self):
        return self.__usuario

    @usuario.setter
    def usuario(self, usuario):
        self.__usuario = usuario

    @property
    def id_proyecto(self):
        return self.__id_proyecto

    @id_proyecto.setter
    def id_proyecto(self, id_proyecto):
        self.__id_proyecto = id_proyecto

    def generateHashId(self):
        self.__id_comentario = hashlib.sha256(uuid.uuid4().bytes).hexdigest()
