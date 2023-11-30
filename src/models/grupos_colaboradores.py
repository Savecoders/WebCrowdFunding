
import re
# uuid: Universally Unique Identifier
import hashlib
import uuid

# usuario grupos
from .user import Usuario


class GruposColaboradores:

    def __init__(self, id_grupo_colaboradores=None, nombre=None, descripcion=None, imagen=None, fecha_creacion=None):
        self.__id_grupo_colaboradores = id_grupo_colaboradores
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__imagen = imagen
        self.__fecha_creacion = fecha_creacion
        self.__usuario_grupos = []

    def __str__(self):
        return f'{self.id_grupo_colaboradores} {self.nombre}'

    # Setters and Getters

    @property
    def id_grupo_colaboradores(self):
        return self.__id_grupo_colaboradores

    @id_grupo_colaboradores.setter
    def id_grupo_colaboradores(self, id_grupo_colaboradores):
        self.__id_grupo_colaboradores = id_grupo_colaboradores

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, checknone):

        if not isinstance(checknone, str):
            raise ValueError("El nombre debe ser unas letras y espacios.")

        # remove spaces
        checknone_strip = checknone.strip()

        if checknone_strip == "":
            raise ValueError("El nombre no puede estar vacío.")

        if (len(checknone) < 4):
            raise ValueError("El nombre debe tener al menos 4 caracteres.")

        self.__nombre = checknone

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, checknone):

        if not isinstance(checknone, str):
            raise ValueError("La descripción debe ser unas letras y espacios.")

        # remove spaces
        checknone_strip = checknone.strip()

        if checknone_strip == "":
            raise ValueError("La descripción no puede estar vacía.")

        if (len(checknone) < 4):
            raise ValueError(
                "La descripción debe tener al menos 4 caracteres.")

        self.__descripcion = checknone

    @property
    def imagen(self):
        return self.__imagen

    @imagen.setter
    def imagen(self, imagen):
        self.__imagen = imagen

    @property
    def fecha_creacion(self):
        return self.__fecha_creacion

    @fecha_creacion.setter
    def fecha_creacion(self, fecha_creacion):
        self.__fecha_creacion = fecha_creacion

    @property
    def usuario_grupos(self) -> list[Usuario]:
        return self.__usuario_grupos

    @usuario_grupos.setter
    def usuario_grupos(self, usuario_grupos: list[Usuario]):

        if not isinstance(usuario_grupos, list):
            raise ValueError("No se puede mostrar la lista de Usuarios.")

        self.__usuario_grupos = usuario_grupos

    # Methods

    def add_usuario_grupo(self, usuario_grupo):
        if not isinstance(usuario_grupo, Usuario):
            raise ValueError(
                "Error al agregar al usuario al grupo")
        self.__usuario_grupos.append(usuario_grupo)

    def generate_hash_id(self):
        self.id_grupo_colaboradores = hashlib.sha256(
            uuid.uuid4().bytes).hexdigest()
