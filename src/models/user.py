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
        self.__nombres = nombres
        self.__contrasena = contrasena
        self.__telefono = telefono
        self.__estado = estado
        self.__email = email
        self.__image_perfil = image_perfil
        self.__pais = pais
        self.__ciudad = ciudad
        self.__fecha_nacimiento = fecha_nacimiento

    def __str__(self):
        return f'{self.__id}, {self.__nombres}, {self.__contrasena}, {self.__telefono}, {self.__estado}, {self.__email}, {self.__image_perfil}, {self.__pais}, {self.__ciudad}, {self.__fecha_nacimiento}'

    # GETTERS AND SETTERS

    @property
    def id_usuario(self):
        return self.__id

    @id_usuario.setter
    def id_usuario(self, id_usuario):
        self.__id = id_usuario

    @property
    def nombres(self):
        return self.__nombres

    @nombres.setter
    def nombres(self, nombres):

        # basic validation
        if not isinstance(nombres, str):
            raise ValueError("El nombre debe ser unas letras y espacios.")
        if nombres == "":
            raise ValueError("El nombre no puede estar vacío.")

        # strip
        nombres = nombres.strip()

        if (len(nombres) < 4):
            raise ValueError("El nombre debe tener al menos 3 caracteres.")

        self.__nombres = nombres

    @property
    def contrasena(self):
        return self.__contrasena

    @contrasena.setter
    def contrasena(self, contrasena):
        if len(contrasena) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")
        self.__contrasena = contrasena

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, telefono):
        if not re.match(r'^\d{10}$', telefono):
            raise ValueError("El teléfono debe ser un número de 10 dígitos.")
        self.__telefono = telefono

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, estado):
        if estado not in ['activo', 'inactivo']:
            raise ValueError("El estado debe ser 'activo' o 'inactivo'.")
        self.__estado = estado

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise ValueError("El email no es válido.")
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
            raise ValueError("La imagen de perfil es requerida.")

        # validate extension
        extensions = ['png', 'jpg', 'jpeg', 'gif']

        # get extension
        extension = image_perfil.filename.split('.')[-1]

        if extension not in extensions:
            raise ValueError(
                f"La extensión de la imagen debe ser {', '.join(extensions)}.")

        # get filename and content type
        # in image profile we don't need filename and content type
        filename = secure_filename(image_perfil.filename)
        content_type = image_perfil.content_type

        # get read image
        self.__image_perfil = image_perfil.read()

    @property
    def pais(self):
        return self.__pais

    @pais.setter
    def pais(self, pais):
        if not isinstance(pais, str):
            raise ValueError("El país debe ser una cadena.")

        pais = pais.strip()

        if (len(pais) < 4):
            raise ValueError("El país debe tener al menos 3 caracteres.")

        self.__pais = pais

    @property
    def ciudad(self):
        return self.__ciudad

    @ciudad.setter
    def ciudad(self, ciudad):
        if not isinstance(ciudad, str):
            raise ValueError("La ciudad debe ser una cadena.")

        ciudad = ciudad.strip()

        if (len(ciudad) < 4):
            raise ValueError("La ciudad debe tener al menos 3 caracteres.")

        self.__ciudad = ciudad

    @property
    def fecha_nacimiento(self):
        return self.__fecha_nacimiento

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, fecha_nacimiento):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', fecha_nacimiento):
            raise ValueError(
                "La fecha de nacimiento debe estar en formato YYYY-MM-DD.")
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
