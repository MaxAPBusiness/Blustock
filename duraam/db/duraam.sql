/*Este es el código SQL de la base de datos*/

/*Crea la tabla de alumnos con los campos id (PK), dni, nombre y 
apellido, curso e email*/
CREATE TABLE IF NOT EXISTS alumnos(
    id VARCHAR(4) PRIMARY KEY,
    dni INTEGER UNIQUE NOT NULL,
    nombre_apellido VARCHAR(50) NOT NULL,
    curso VARCHAR(2) NOT NULL,
    email VARCHAR(320)
);

/*Crea la tabla de alumnos historicos con los campos id (PK), dni,
nombre, y apellido, curso, fecha de salida e email*/
CREATE TABLE IF NOT EXISTS alumnos_historicos(
    id VARCHAR(4) PRIMARY KEY,
    dni INTEGER UNIQUE NOT NULL,
    nombre_apellido VARCHAR(50) NOT NULL,
    curso VARCHAR(2) NOT NULL,
    fecha_salida VARCHAR(10) NOT NULL,
    email VARCHAR(320)
);

/*Crea la tabla de herramientas con los campos id (PK), descripción, 
cantidad en condiciones, cantidad en reparación, cantidad de baja, 
total, id de grupo e id de subgrupo.*/
CREATE TABLE IF NOT EXISTS herramientas(
    id VARCHAR(4) PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    cant_condiciones INTEGER,
    cant_reparacion INTEGER,
    cant_baja INTEGER,
    total INTEGER,
    grupo VARCHAR(50),
    subgrupo VARCHAR(50),
    FOREIGN KEY(grupo) REFERENCES grupos(id) ON DELETE CASCADE,
    FOREIGN KEY(subgrupo) REFERENCES subgrupos(id) ON DELETE SET NULL
);

/*Crea la tabla de profesores con los campos id (PK) y nombre y apellido*/
CREATE TABLE IF NOT EXISTS profesores(
    id VARCHAR(4) PRIMARY KEY,
    dni INTEGER UNIQUE NOT NULL,
    nombre_apellido VARCHAR(50) NOT NULL,
    email VARCHAR(320)
);

CREATE TABLE IF NOT EXISTS profesores_historicos(
    id VARCHAR(4) PRIMARY KEY,
    dni INTEGER UNIQUE NOT NULL,
    nombre_apellido VARCHAR(50) NOT NULL,
    fecha_pase VARCHAR(10),
    email VARCHAR(320)
);

/*Crea la tabla de alumnos con los campos id (PK), fecha, alumno, nombre y apellido y email*/
CREATE TABLE IF NOT EXISTS turno_panol(
    id INTEGER PRIMARY KEY,
    fecha VARCHAR(12),
    id_alumno INTEGER,
    hora_ingreso VARCHAR(12),
    hora_egreso VARCHAR(12),
    prof_ingreso INTEGER,
    prof_egreso INTEGER
);

/*Crea la tabla de movimiento de herramientas con los campos id_herramienta, id_alumno, fecha, cantidad, 
tipo (ingreso o devolución y el id del turno del pañol.*/
CREATE TABLE IF NOT EXISTS movimientos_herramientas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_herramienta INTEGER,
    id_persona INTEGER,
    clase INTEGER,
    fecha_hora VARCHAR(24),
    cantidad INTEGER,
    tipo INTEGER,
    id_turno_panol INTEGER,
    FOREIGN KEY(id_herramienta) REFERENCES herramientas(id) ON DELETE CASCADE,
    FOREIGN KEY(id_turno_panol) REFERENCES turno_panol(id) ON DELETE CASCADE
);

/*Crea la tabla de usuarios. Ignorar por ahora*/
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario VARCHAR(20) UNIQUE NOT NULL,
    contrasena VARCHAR(75),
    nombre_apellido VARCHAR(35)
);

CREATE TABLE IF NOT EXISTS administradores(
    id INTEGER PRIMARY KEY,
    usuario VARCHAR(20) UNIQUE NOT NULL,
    contrasena VARCHAR(75),
    nombre_apellido VARCHAR(35)
);

CREATE TABLE IF NOT EXISTS solicitudes(
    usuario VARCHAR(20) UNIQUE NOT NULL,
    contrasena VARCHAR(75),
    nombre_apellido VARCHAR(35),
    estado INTEGER
);

/*Crea la tabla de usuarios. Ignorar por ahora*/
CREATE TABLE IF NOT EXISTS grupos(
    id VARCHAR(40) PRIMARY KEY
);

/*Crea la tabla de usuarios. Ignorar por ahora*/
CREATE TABLE IF NOT EXISTS subgrupos(
    id VARCHAR(40) PRIMARY KEY,
    grupo VARCHAR(40),
    FOREIGN KEY(grupo) REFERENCES grupos(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS HISTORIAL_DE_CAMBIOS(
    id_usuario INTEGER,
    rol INTEGER,
    fecha_hora VARCHAR(30) NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    tabla VARCHAR(20) NOT NULL,
    id_fila VARCHAR(4),
    datos_viejos VARCHAR(400),
    datos_nuevos VARCHAR(400)
)