CREATE TABLE USUARIOS (
  IDUSUARIO NUMBER PRIMARY KEY,
  NOMBRES VARCHAR2(50 CHAR) NOT NULL,
  CONTRASENA VARCHAR2(255 CHAR) NOT NULL,
  TELEFONO VARCHAR2(15 CHAR) NOT NULL,
  ESTADO VARCHAR2(20 CHAR) NOT NULL,
  EMAIL VARCHAR2(100 CHAR) UNIQUE,
  IMAGENPERFIL VARCHAR2(50 CHAR),
  PAIS VARCHAR2(100 CHAR) NOT NULL,
  CIUDAD VARCHAR2(100 CHAR) NOT NULL,
  FECHANACIMIENTO DATE
);

CREATE TABLE GRUPOSCOLABORADORES (
  IDGRUPO NUMBER PRIMARY KEY,
  NOMBREGRUPO VARCHAR2(50 CHAR)
);

CREATE TABLE USUARIOSGRUPOS (
  IDUSUARIO NUMBER,
  IDGRUPO NUMBER,
  PRIMARY KEY (IDUSUARIO, IDGRUPO)
);

CREATE TABLE ROL (
  IDROL NUMBER PRIMARY KEY,
  PERMISO VARCHAR2(150 CHAR),
  DESCRIPCION VARCHAR2(50 CHAR) NOT NULL
);

CREATE TABLE USUARIOROL (
  IDUSUARIO NUMBER,
  IDROL NUMBER,
  PRIMARY KEY (IDUSUARIO, IDROL)
);

CREATE TABLE PROYECTOS (
  IDPROYECTO NUMBER PRIMARY KEY,
  IDEA VARCHAR2(200 CHAR) NOT NULL,
  NOMBRE VARCHAR2(100 CHAR) NOT NULL,
  FECHALIMITE DATE,
  PRESENTACION CLOB NOT NULL,
  PRESUPUESTO NUMBER(10, 2),
  METAALCANZADA NUMBER(1) DEFAULT 0,
  IDESTADO NUMBER,
  IDGRUPO NUMBER,
  IDIMAGENES NUMBER,
  IDREDES NUMBER,
  IDRECOMPONESA NUMBER
);

CREATE TABLE PROYECTOSCATEGORIAS (
  IDPROYECTO NUMBER,
  IDCATEGORIA NUMBER,
  PRIMARY KEY (IDPROYECTO, IDCATEGORIA)
);

CREATE TABLE CATEGORIAS (
  IDCATEGORIA NUMBER PRIMARY KEY,
  IDSUBCATEGORIA NUMBER,
  NOMBRECATEGORIA VARCHAR2(50 CHAR) NOT NULL
);

CREATE TABLE SUBCATEGORIAS (
  IDSUBCATEGORIA NUMBER PRIMARY KEY,
  NOMBRESUBCATEGORIA VARCHAR2(50 CHAR)
);

CREATE TABLE ESTADOS (
  IDESTADO NUMBER PRIMARY KEY,
  NOMBREESTADO VARCHAR2(20 CHAR)
);

CREATE TABLE COMENTARIOS (
  IDCOMENTARIO NUMBER PRIMARY KEY,
  COMENTARIO VARCHAR2(400 CHAR),
  FECHACOMENTARIO DATE,
  IDUSUARIO NUMBER,
  IDPROYECTO NUMBER
);

CREATE TABLE IMAGENESPROYECTO (
  IDIMAGENES NUMBER PRIMARY KEY,
  ARCHIVO VARCHAR2(200 CHAR) NOT NULL
);

CREATE TABLE DONACION (
  IDDONACION NUMBER PRIMARY KEY,
  MONTO NUMBER,
  FECHADONACION DATE,
  IDUSUARIO NUMBER,
  IDPROYECTO NUMBER,
  IDMETODOPAGO NUMBER
);

CREATE TABLE PROYECTOS_DONACION (
  IDPROYECTO NUMBER,
  IDDONACION NUMBER,
  PRIMARY KEY (IDPROYECTO, IDDONACION),
  FOREIGN KEY (IDPROYECTO) REFERENCES PROYECTOS(IDPROYECTO),
  FOREIGN KEY (IDDONACION) REFERENCES DONACION(IDDONACION)
);

CREATE TABLE METODOPAGO (
  IDMETODOPAGO NUMBER PRIMARY KEY,
  MONTO NUMBER NOT NULL,
  FECHA DATE,
  IDPAYPAL NUMBER,
  IDCUENTABANCARIA NUMBER,
  IDTARJETA NUMBER
);

CREATE TABLE PAYPAL (
  IDPAYPAL NUMBER PRIMARY KEY,
  EMAIL VARCHAR2(160 CHAR)
);

CREATE TABLE TARJETA (
  IDTARJETA NUMBER PRIMARY KEY,
  BANCO CLOB,
  TELEFONO VARCHAR2(15 CHAR),
  DVD VARCHAR2(10 CHAR),
  FECHAVENCIMIENTO DATE
);

CREATE TABLE IDCUENTABANCARIA (
  IDCUENTABANCARIA NUMBER PRIMARY KEY,
  BANCO CLOB,
  TIPO VARCHAR2(100 CHAR),
  FECHAVENCIMIENTO DATE
);

CREATE TABLE REDES (
  IDREDES NUMBER PRIMARY KEY,
  NOMBRE VARCHAR2(150 CHAR) NOT NULL,
  URL VARCHAR2(150 CHAR) NOT NULL
);

CREATE TABLE RECOMPENSA (
  IDRECOMPENSA NUMBER PRIMARY KEY,
  FECHAADQUISICION TIMESTAMP DEFAULT (SYSTIMESTAMP),
  AGRADECIMIENTO CLOB
);

ALTER TABLE USUARIOSGRUPOS ADD CONSTRAINT FK_USUARIOSGRUPOS_USUARIOS FOREIGN KEY (IDUSUARIO) REFERENCES USUARIOS(IDUSUARIO);

ALTER TABLE USUARIOSGRUPOS ADD CONSTRAINT FK_USUARIOSGRUPOS_GRUPOSCOLABORADORES FOREIGN KEY (IDGRUPO) REFERENCES GRUPOSCOLABORADORES(IDGRUPO);

ALTER TABLE USUARIOROL ADD CONSTRAINT FK_USUARIOROL_USUARIOS FOREIGN KEY (IDUSUARIO) REFERENCES USUARIOS(IDUSUARIO);

ALTER TABLE USUARIOROL ADD CONSTRAINT FK_USUARIOROL_ROL FOREIGN KEY (IDROL) REFERENCES ROL(IDROL);

ALTER TABLE PROYECTOS ADD CONSTRAINT FK_PROYECTOS_GRUPOSCOLABORADORES FOREIGN KEY (IDGRUPO) REFERENCES GRUPOSCOLABORADORES(IDGRUPO);

ALTER TABLE PROYECTOSCATEGORIAS ADD CONSTRAINT FK_PROYECTOSCATEGORIAS_PROYECTOS FOREIGN KEY (IDPROYECTO) REFERENCES PROYECTOS(IDPROYECTO);

ALTER TABLE PROYECTOSCATEGORIAS ADD CONSTRAINT FK_PROYECTOSCATEGORIAS_CATEGORIAS FOREIGN KEY (IDCATEGORIA) REFERENCES CATEGORIAS(IDCATEGORIA);

ALTER TABLE CATEGORIAS ADD CONSTRAINT FK_CATEGORIAS_SUBCATEGORIAS FOREIGN KEY (IDSUBCATEGORIA) REFERENCES SUBCATEGORIAS(IDSUBCATEGORIA);

ALTER TABLE COMENTARIOS ADD CONSTRAINT FK_COMENTARIOS_USUARIOS FOREIGN KEY (IDUSUARIO) REFERENCES USUARIOS(IDUSUARIO);

ALTER TABLE COMENTARIOS ADD CONSTRAINT FK_COMENTARIOS_PROYECTOS FOREIGN KEY (IDPROYECTO) REFERENCES PROYECTOS(IDPROYECTO);

ALTER TABLE DONACION ADD CONSTRAINT FK_DONACION_USUARIOS FOREIGN KEY (IDUSUARIO) REFERENCES USUARIOS(IDUSUARIO);

ALTER TABLE DONACION ADD CONSTRAINT FK_DONACION_PROYECTOS FOREIGN KEY (IDPROYECTO) REFERENCES PROYECTOS(IDPROYECTO);

ALTER TABLE DONACION ADD CONSTRAINT FK_DONACION_METODOPAGO FOREIGN KEY (IDMETODOPAGO) REFERENCES METODOPAGO(IDMETODOPAGO);

ALTER TABLE METODOPAGO ADD CONSTRAINT FK_METODOPAGO_PAYPAL FOREIGN KEY (IDPAYPAL) REFERENCES PAYPAL(IDPAYPAL);

ALTER TABLE METODOPAGO ADD CONSTRAINT FK_METODOPAGO_IDCUENTABANCARIA FOREIGN KEY (IDCUENTABANCARIA) REFERENCES IDCUENTABANCARIA(IDCUENTABANCARIA);

ALTER TABLE METODOPAGO ADD CONSTRAINT FK_METODOPAGO_TARJETA FOREIGN KEY (IDTARJETA) REFERENCES TARJETA(IDTARJETA);