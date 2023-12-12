# secure_filename: Valida el nombre de un archivo
from werkzeug.utils import secure_filename
import hashlib
import uuid
import os
import base64
import re
class Proyecto:
    def __init__(self, idProyecto=None, idea=None, nombre=None, fechaLimite=None, presentacion=None, presupuesto=None, recompensa=None, metaAlcanzada=None, estado=None):
        self.__id = idProyecto
        self.__idea = idea
        self.__nombre = nombre
        self.__fechaLimite = fechaLimite
        self.__presentacion = presentacion
        self.__presupuesto = presupuesto
        self.__recompensa = recompensa
        self.__metaAlcanzada = metaAlcanzada
        self.__estado = estado
        self.__idgruppo= None
        self.__iddonacion= None
    def __str__(self):
        return f'{self.__id}, {self.__idea}, {self.__nombre}, {self.__fechaLimite}, {self.__presentacion}, {self.__presupuesto}, {self.__recompensa}, {self.__metaAlcanzada}, {self.__estado}'
    @property
    def idProyecto(self):
        return self.__id

    @idProyecto.setter
    def idProyecto(self, idProyecto):
        self.__id = idProyecto

    @property
    def idea (self):
        return self.__idea
    @idea.setter
    def idea(self, idea):
        if not isinstance(idea, str):
            raise ValueError("The name must be a string.")
        if idea == "":
            raise ValueError("The name can't be empty.")

        # strip
        ideaStrip = idea.strip()

        if (len(ideaStrip) < 30):
            raise ValueError("The name must have at least 30 characters.")
        self.__idea = idea
    @property
    def nombre (self):
        return self.__nombre
    @nombre.setter
    def nombre(self, nombre):
        if not isinstance(nombre, str):
            raise ValueError("The name must be a string.")
        if nombre == "":
            raise ValueError("The name can't be empty.")

        # strip
        nombreStrip = nombre.strip()

        if (len(nombreStrip) < 10):
            raise ValueError("The name must have at least 10 characters.")

        self.__nombre = nombre

    @property
    def fechaLimite (self):
        return self.__fechaLimite
    @fechaLimite.setter
    def fechaLimite(self, fechaLimite):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', fechaLimite):
            raise ValueError("The date of limite be in the format YYYY-MM-DD.")
        self.__fechaLimite = fechaLimite     
    @property
    def presentacion (self):
        return self.__presentacion
    @fechaLimite.setter
    def presentacion(self, presentacion):
        if not presentacion:
            raise ValueError("required image.")

        # validate extension
        extensions = ['png', 'jpg', 'jpeg', 'gif']

        # get extension
        extension = presentacion.filename.split('.')[-1]

        if extension not in extensions:
            raise ValueError(
                f"The extension of the image must be{', '.join(extensions)}.")

        # get filename and content type
        # in image profile we don't need filename and content type
        filename = secure_filename(presentacion.filename)
        content_type = presentacion.content_type

        # get read image
        self.__presentacion = presentacion.read()

    def insert_binary_image(self, image):
        self.__presentacion = image
    @property
    def presupuesto  (self):
        return self.__presupuesto
    @presupuesto.setter
    def presupuesto(self, presupuesto):
        if (presupuesto<0):
            raise ValueError("el presupuesto debe ser postivo.")
        self.__presupuesto = presupuesto  
    @property
    def recompensa  (self):
        return self.__recompensa
    @recompensa.setter
    def recompensa(self, recompensa):
        if (recompensa<0):
            raise ValueError("el presupuesto debe ser postivo.")
        self.__recompensa = recompensa
    @property
    def metaAlcanzada  (self):
        return self.__metaAlcanzada
    @metaAlcanzada.setter
    def metaAlcanzada(self, metaAlcanzada):
        if (metaAlcanzada<0):
            raise ValueError("el presupuesto debe ser postivo.")
        self.__metaAlcanzada = metaAlcanzada
    @property
    def estado  (self):
        return self.__estado
    @estado.setter
    def estado(self, estado):
        if not isinstance(estado, str):
            raise ValueError("The name must be a string.")
        if estado == "":
            raise ValueError("The name can't be empty.")

        # strip
        estadoStrip = estado.strip()

        if (len(estado) < 5):
            raise ValueError("The name must have at least 5 characters.")
        self.__estado = estado
    def generateHashId(self):
        self.__id = hashlib.sha256(uuid.uuid4().bytes).hexdigest()
    def get_binary_presentacion(self):
        return self.__presentacion
    def inserdao(self):
        return (self.__id, self.__idea, self.__nombre, self.__fechaLimite,self.get_binary_presentacion(), self.__presupuesto, self.__recompensa, self.__metaAlcanzada, self.__estado)