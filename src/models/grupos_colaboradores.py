
class GruposColaboradores:

    def __init__(self, id_grupo_colaboradores, nombre):
        self.id_grupo_colaboradores = id_grupo_colaboradores
        self.nombre = nombre

    def __str__(self):
        return f'{self.id_grupo_colaboradores} {self.nombre}'

    # Setters and Getters

    @property
    def id_grupo_colaboradores(self):
        return self.__id_grupo_colaboradores

    @property
    def nombre(self):
        return self.__nombre

    @id_grupo_colaboradores.setter
    def id_grupo_colaboradores(self, id_grupo_colaboradores):
        self.__id_grupo_colaboradores = id_grupo_colaboradores
