import re
# uuid: Universally Unique Identifier
import hashlib
import uuid

# generate_password_hash: Genera un hash de la contraseña
from werkzeug.security import generate_password_hash

# secure_filename: Valida el nombre de un archivo
from werkzeug.utils import secure_filename
import os
import base64

# desing pattern: Data Transfer Object - DTO


class Usuario:

    # contructor
    def __init__(self, id_usuario=None, nombres=None, contrasena=None, telefono=None, estado=None, email=None, image_perfil=None, pais=None, ciudad=None, fecha_nacimiento=None):
        self.__id = id_usuario
        self.__nombre = nombres
        self.__contrasena = contrasena
        self.__telefono = telefono
        self.__estado = estado
        self.__email = email
        self.__image_perfil = image_perfil
        self.__pais = pais
        self.__ciudad = ciudad
        self.__fecha_nacimiento = fecha_nacimiento

    def __str__(self):
        return f'{self.__id}, {self.__nombre}, {self.__contrasena}, {self.__telefono}, {self.__estado}, {self.__email}, {self.__image_perfil}, {self.__pais}, {self.__ciudad}, {self.__fecha_nacimiento}'

    # GETTERS AND SETTERS

    @property
    def id_usuario(self):
        return self.__id

    @id_usuario.setter
    def id_usuario(self, id_usuario):
        self.__id = id_usuario

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):

        # basic validation
        if not isinstance(nombre, str):
            raise ValueError("The name must be a string.")
        if nombre == "":
            raise ValueError("The name can't be empty.")

        # strip
        nombreStrip = nombre.strip()

        if (len(nombreStrip) < 4):
            raise ValueError("The name must have at least 3 characters.")

        self.__nombre = nombre

    @property
    def contrasena(self):
        return self.__contrasena

    @contrasena.setter
    def contrasena(self, contrasena):
        if len(contrasena) < 8:
            raise ValueError("The password must have at least 8 characters.")
        self.__contrasena = contrasena

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, telefono):
        if not re.match(r'^\d{10}$', telefono):
            raise ValueError("The phone number must have 10 digits.")
        self.__telefono = telefono

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, estado):
        if estado not in ['activo', 'inactivo']:
            raise ValueError("The state must be active or inactive.")
        self.__estado = estado

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise ValueError("The email must be a valid email.")
        self.__email = email

    @property
    def image_perfil(self):
        if self.__image_perfil:
            # Read bytes from LOB
            image_bytes = self.__image_perfil
            # Convert bytes to base64
            image_encoded = base64.b64encode(image_bytes).decode('utf-8')
            # Create data URL
            image_data_url = f"data:image/png;base64,{image_encoded}"
            return image_data_url
        else:
            return None

    @image_perfil.setter
    def image_perfil(self, image_perfil):

        # Save image

        # validate image
        if not image_perfil:
            raise ValueError("required image.")

        # validate extension
        extensions = ['png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', "jfif"]

        # get extension
        extension = image_perfil.filename.split('.')[-1]

        if extension not in extensions:
            raise ValueError(
                f"The extension of the image must be{', '.join(extensions)}.")

        # get filename and content type
        # in image profile we don't need filename and content type
        filename = secure_filename(image_perfil.filename)
        content_type = image_perfil.content_type

        # get read image
        self.__image_perfil = image_perfil.read()

    def insert_binary_image(self, image):
        self.__image_perfil = image

    @property
    def pais(self):
        return self.__pais

    @pais.setter
    def pais(self, pais):
        if not isinstance(pais, str):
            raise ValueError("The country must be a string.")

        pais = pais.strip()

        if (len(pais) < 4):
            raise ValueError("The country must have at least 3 characters.")

        self.__pais = pais

    @property
    def ciudad(self):
        return self.__ciudad

    @ciudad.setter
    def ciudad(self, ciudad):
        if not isinstance(ciudad, str):
            raise ValueError("The city must be a string.")

        ciudad = ciudad.strip()

        if (len(ciudad) < 4):
            raise ValueError("The city must have at least 3 characters.")

        self.__ciudad = ciudad

    @property
    def fecha_nacimiento(self):
        return self.__fecha_nacimiento

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, fecha_nacimiento):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_nacimiento):
            raise ValueError(
                "The date of birth must be in the format YYYY-MM-DD.")
        self.__fecha_nacimiento = fecha_nacimiento

    # METODOS

    def generateHashId(self):
        self.__id = hashlib.sha256(uuid.uuid4().bytes).hexdigest()

    def generateHashPassword(self):
        self.__contrasena = generate_password_hash(self.__contrasena)

    def generateEstado(self):
        self.__estado = 'activo'

    def load_image_perfil(self):
        if self.__image_perfil:
            # Read bytes from LOB
            self.__image_perfil = self.__image_perfil.read()

    def get_binary_image_perfil(self):
        return self.__image_perfil

    def inserdao(self):
        return (self.__id, self.__nombre, self.__contrasena, self.__telefono, self.__estado, self.__email, self.get_binary_image_perfil(), self.__pais, self.__ciudad, self.__fecha_nacimiento)
