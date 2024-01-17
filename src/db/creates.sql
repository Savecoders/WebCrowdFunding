CREATE TABLE USUARIOS (
  IDUSUARIO VARCHAR(255) PRIMARY KEY,
  NOMBRES VARCHAR(50) NOT NULL,
  CONTRASENA VARCHAR(255) NOT NULL,
  TELEFONO VARCHAR(15) NOT NULL,
  ESTADO VARCHAR(20) NOT NULL,
  EMAIL VARCHAR(100) UNIQUE,
  IMAGENPERFIL BYTEA,
  PAIS VARCHAR(100) NOT NULL,
  CIUDAD VARCHAR(100) NOT NULL,
  FECHANACIMIENTO VARCHAR(15)
);

CREATE TABLE GRUPOSCOLABORADORES (
  IDGRUPO VARCHAR(255) PRIMARY KEY,
  NOMBREGRUPO VARCHAR(80),
  DESCRIPCION VARCHAR(120),
  IMAGEN BYTEA,
  FECHACREACION VARCHAR(120)
);

CREATE TABLE USUARIOSGRUPOS (
  IDUSUARIO VARCHAR(255),
  IDGRUPO VARCHAR(255),
  PRIMARY KEY (IDUSUARIO, IDGRUPO)
);

CREATE TABLE ROL (
  IDROL VARCHAR(255) PRIMARY KEY,
  PERMISO VARCHAR(150),
  DESCRIPCION VARCHAR(50) NOT NULL
);

CREATE TABLE USUARIOROL (
  IDUSUARIO VARCHAR(255),
  IDROL VARCHAR(255),
  PRIMARY KEY (IDUSUARIO, IDROL)
);

CREATE TABLE PROYECTOS (
  IDPROYECTO VARCHAR(255) PRIMARY KEY,
  NOMBRE VARCHAR(100) NOT NULL,
  IDEA VARCHAR(400) NOT NULL,
  DESCRIPCION VARCHAR(500),
  FECHALIMITE VARCHAR(30),
  PRESENTACION BYTEA NOT NULL,
  PRESUPUESTO NUMERIC(10, 2),
  RECOMPENSA VARCHAR(255),
  METAALCANZADA NUMERIC DEFAULT 0,
  ESTADO VARCHAR(255),
  IDGRUPO VARCHAR(255),
  FOREIGN KEY (IDGRUPO) REFERENCES GRUPOSCOLABORADORES(IDGRUPO)
);

CREATE TABLE PROYECTOSCATEGORIAS (
  IDPROYECTO VARCHAR(255),
  IDCATEGORIA VARCHAR(255),
  PRIMARY KEY (IDPROYECTO, IDCATEGORIA)
);

CREATE TABLE CATEGORIAS (
  IDCATEGORIA VARCHAR(255) PRIMARY KEY,
  IDSUBCATEGORIA VARCHAR(255),
  NOMBRECATEGORIA VARCHAR(50) NOT NULL
);

CREATE TABLE SUBCATEGORIAS (
  IDSUBCATEGORIA VARCHAR(255) PRIMARY KEY,
  NOMBRESUBCATEGORIA VARCHAR(50)
);

CREATE TABLE ESTADOS (
  IDESTADO VARCHAR(255) PRIMARY KEY,
  NOMBREESTADO VARCHAR(20)
);

CREATE TABLE COMENTARIOS (
  IDCOMENTARIO VARCHAR(255) PRIMARY KEY,
  COMENTARIO VARCHAR(400),
  FECHACOMENTARIO DATE,
  IDUSUARIO VARCHAR(255),
  IDPROYECTO VARCHAR(255)
);

CREATE TABLE IMAGENESPROYECTO (
  IDIMAGENES VARCHAR(255) PRIMARY KEY,
  ARCHIVO VARCHAR(200) NOT NULL
);

CREATE TABLE DONACION (
  IDDONACION VARCHAR(255) PRIMARY KEY,
  MONTO NUMERIC NOT NULL,
  FECHADONACION DATE,
  IDUSUARIO VARCHAR(255),
  IDPROYECTO VARCHAR(255)
);

CREATE TABLE PROYECTOS_DONACION (
  IDPROYECTO VARCHAR(255),
  IDDONACION VARCHAR(255),
  PRIMARY KEY (IDPROYECTO, IDDONACION),
  FOREIGN KEY (IDPROYECTO) REFERENCES PROYECTOS(IDPROYECTO),
  FOREIGN KEY (IDDONACION) REFERENCES DONACION(IDDONACION)
);

CREATE TABLE METODOPAGO (
  IDMETODOPAGO VARCHAR(255) PRIMARY KEY,
  MONTO NUMERIC NOT NULL,
  FECHA DATE,
  IDPAYPAL VARCHAR(255),
  IDCUENTABANCARIA VARCHAR(255),
  IDTARJETA VARCHAR(255)
);

CREATE TABLE PAYPAL (
  IDPAYPAL VARCHAR(255) PRIMARY KEY,
  EMAIL VARCHAR(160)
);

CREATE TABLE TARJETA (
  IDTARJETA VARCHAR(255) PRIMARY KEY,
  BANCO TEXT,
  TELEFONO VARCHAR(15),
  DVD VARCHAR(10),
  FECHAVENCIMIENTO DATE
);

CREATE TABLE IDCUENTABANCARIA (
  IDCUENTABANCARIA VARCHAR(255) PRIMARY KEY,
  BANCO TEXT,
  TIPO VARCHAR(100),
  FECHAVENCIMIENTO DATE
);

CREATE TABLE REDES (
  IDREDES VARCHAR(255) PRIMARY KEY,
  NOMBRE VARCHAR(150) NOT NULL,
  URL VARCHAR(150) NOT NULL
);

CREATE TABLE RECOMPENSA (
  IDRECOMPENSA VARCHAR(255) PRIMARY KEY,
  FECHAADQUISICION TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  AGRADECIMIENTO TEXT
);

ALTER TABLE
  USUARIOSGRUPOS
ADD
  CONSTRAINT FK_USUARIOSGRUPOS_USUARIOS FOREIGN KEY (IDUSUARIO) REFERENCES USUARIOS(IDUSUARIO);

ALTER TABLE
  USUARIOSGRUPOS
ADD
  CONSTRAINT FK_USUARIOSGRUPOS_GRUPOSCOLABORADORES FOREIGN KEY (IDGRUPO) REFERENCES GRUPOSCOLABORADORES(IDGRUPO);

ALTER TABLE
  USUARIOROL
ADD
  CONSTRAINT FK_USUARIOROL_USUARIOS FOREIGN KEY (IDUSUARIO) REFERENCES USUARIOS(IDUSUARIO);

ALTER TABLE
  USUARIOROL
ADD
  CONSTRAINT FK_USUARIOROL_ROL FOREIGN KEY (IDROL) REFERENCES ROL(IDROL);

ALTER TABLE
  PROYECTOSCATEGORIAS
ADD
  CONSTRAINT FK_PROYECTOSCATEGORIAS_PROYECTOS FOREIGN KEY (IDPROYECTO) REFERENCES PROYECTOS(IDPROYECTO);

ALTER TABLE
  PROYECTOSCATEGORIAS
ADD
  CONSTRAINT FK_PROYECTOSCATEGORIAS_CATEGORIAS FOREIGN KEY (IDCATEGORIA) REFERENCES CATEGORIAS(IDCATEGORIA);

ALTER TABLE
  CATEGORIAS
ADD
  CONSTRAINT FK_CATEGORIAS_SUBCATEGORIAS FOREIGN KEY (IDSUBCATEGORIA) REFERENCES SUBCATEGORIAS(IDSUBCATEGORIA);

ALTER TABLE
  COMENTARIOS
ADD
  CONSTRAINT FK_COMENTARIOS_USUARIOS FOREIGN KEY (IDUSUARIO) REFERENCES USUARIOS(IDUSUARIO);

ALTER TABLE
  COMENTARIOS
ADD
  CONSTRAINT FK_COMENTARIOS_PROYECTOS FOREIGN KEY (IDPROYECTO) REFERENCES PROYECTOS(IDPROYECTO);

ALTER TABLE
  IMAGENESPROYECTO
ADD
  CONSTRAINT FK_IMAGENESPROYECTO_PROYECTOS FOREIGN KEY (IDIMAGENES) REFERENCES PROYECTOS(IDPROYECTO);

ALTER TABLE
  DONACION
ADD
  CONSTRAINT FK_DONACION_USUARIOS FOREIGN KEY (IDUSUARIO) REFERENCES USUARIOS(IDUSUARIO);

ALTER TABLE
  DONACION
ADD
  CONSTRAINT FK_DONACION_PROYECTOS FOREIGN KEY (IDPROYECTO) REFERENCES PROYECTOS(IDPROYECTO);

ALTER TABLE
  PROYECTOS_DONACION
ADD
  CONSTRAINT FK_PROYECTOS_DONACION_PROYECTOS FOREIGN KEY (IDPROYECTO) REFERENCES PROYECTOS(IDPROYECTO);

ALTER TABLE
  PROYECTOS_DONACION
ADD
  CONSTRAINT FK_PROYECTOS_DONACION_DONACION FOREIGN KEY (IDDONACION) REFERENCES DONACION(IDDONACION);