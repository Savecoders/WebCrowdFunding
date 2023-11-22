# desing pattern: Data Transfer Object - DTO
class Usuarios:
    def __init__(self, id_usuario, nombres, contrasena, telefono, estado, email, image_perfil, pais, ciudad, fecha_nacimiento):
        self._id = id_usuario
        self._nombres = nombres
        self._contrasena = contrasena
        self._telefono = telefono
        self._estado = estado
        self._email = email
        self._image_perfil = image_perfil
        self._pais = pais
        self._ciudad = ciudad
        self._fecha_nacimiento = fecha_nacimiento

    def __str__(self):
        return f'{self._id}, {self._nombres}, {self._contrasena}, {self._telefono}, {self._estado}, {self._email}, {self._image_perfil}, {self._pais}, {self._ciudad}, {self._fecha_nacimiento}'

    # GETTERS AND SETTERS

    @property
    def id_usuario(self):
        return self._id

    @property
    def nombres(self):
        return self._nombres

    @nombres.setter
    def nombres(self, nombres):
        self._nombres = nombres

    @property
    def contrasena(self):
        return self._contrasena

    @contrasena.setter
    def contrasena(self, contrasena):
        self._contrasena = contrasena

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, telefono):
        self._telefono = telefono

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, estado):
        self._estado = estado

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def image_perfil(self):
        return self._image_perfil

    @image_perfil.setter
    def image_perfil(self, image_perfil):
        self._image_perfil = image_perfil

    @property
    def pais(self):
        return self._pais

    @pais.setter
    def pais(self, pais):
        self._pais = pais

    @property
    def ciudad(self):
        return self._ciudad

    @ciudad.setter
    def ciudad(self, ciudad):
        self._ciudad = ciudad

    @property
    def fecha_nacimiento(self):
        return self._fecha_nacimiento

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, fecha_nacimiento):
        self._fecha_nacimiento = fecha_nacimiento
