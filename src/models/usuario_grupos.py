
from .user import Usuario


class UsuarioGrupo:
    def __init__(self, usuario=None, grupo=None):
        self.__usuario = usuario
        self.__grupo = grupo

    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @usuario.setter
    def usuario(self, usuario: Usuario):

        # basic validation

        if not isinstance(usuario, Usuario) and usuario != None:
            raise ValueError("No se ha ingresado el Usuario")

        if usuario.id_usuario == None:
            raise ValueError("El usuario debe tener un id.")

        self.__usuario = usuario
