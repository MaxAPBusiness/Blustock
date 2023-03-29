/*Este es el código SQL de la base de datos*/

/*Crea la tabla de personal con los campos dni, 
nombre_apellido, curso, usuario, contrasena y rango.
En esta tabla estarán ingresados los usuarios,
alumnos y personal no docente de la institución*/
CREATE TABLE IF NOT EXISTS personal(
    dni INTEGER PRIMARY KEY NOT NULL,
    nombre_apellido VARCHAR(50) NOT NULL,
    curso VARCHAR(20),
    usuario VARCHAR(20) UNIQUE NOT NULL,
    contrasena VARCHAR(75) NOT NULL,
    rango INTEGER NOT NULL
);

/*Crea la tabla de stock con los campos id (PK), descripción, 
cantidad en condiciones, cantidad en reparación, cantidad de baja 
e id de subgrupo. En esta tabla estarán ingresadas las herramientas
y los insumos*/
CREATE TABLE IF NOT EXISTS stock(
    id INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
    desc VARCHAR(100) NOT NULL,
    cant_condiciones INTEGER NOT NULL,
    cant_reparacion INTEGER,
    cant_baja INTEGER,
    id_subgrupo VARCHAR(50),
    FOREIGN KEY(id_subgrupo) REFERENCES subgrupos(id) ON DELETE CASCADE
);

/*Crea la tabla de turnos con los campos id (PK),
fecha, id_panolero, hora de ingreso, hora de egreso, profesor
de ingreso y profesor de egreso.*/
CREATE TABLE IF NOT EXISTS turnos(
    id INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
    fecha VARCHAR(12),
    id_panolero INTEGER,
    hora_ingreso VARCHAR(12),
    hora_egreso VARCHAR(12),
    prof_ingreso INTEGER NOT NULL,
    prof_egreso INTEGER,
    FOREIGN KEY(id_panolero) REFERENCES personal(dni) ON DELETE CASCADE,
    FOREIGN KEY(prof_ingreso) REFERENCES personal(dni) ON DELETE CASCADE,
    FOREIGN KEY(prof_egreso) REFERENCES personal(dni) ON DELETE CASCADE
);

/*Crea la tabla de movimientos con los campos id, id_herramienta, 
id_persona, fecha_hora, cantidad, tipo (ingreso, retiro o devolución),
estado (si la herramienta vuelve en condiciones o rota) y el id del turno del pañol.*/
CREATE TABLE IF NOT EXISTS movimientos(
    id INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
    id_herramienta INTEGER NOT NULL,
    id_persona INTEGER NOT NULL,
    fecha_hora VARCHAR(24) NOT NULL,
    cantidad INTEGER NOT NULL,
    tipo INTEGER NOT NULL,
    estado INTEGER NOT NULL,
    id_turno INTEGER NOT NULL,
    FOREIGN KEY(id_herramienta) REFERENCES herramientas(id) ON DELETE CASCADE,
    FOREIGN KEY(id_personas) REFERENCES personal(dni) ON DELETE CASCADE,
    FOREIGN KEY(id_turno) REFERENCES turno_panol(id) ON DELETE CASCADE
);

/*Crea la tabla de grupos con el campo id y descripción*/
CREATE TABLE IF NOT EXISTS grupos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    desc VARCHAR(40) NOT NULL
);

/*Crea la tabla de subgrupos con el campo id, descripcion
y el id de grupo al que pertenece*/
CREATE TABLE IF NOT EXISTS subgrupos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    desc VARCHAR(40),
    id_grupo VARCHAR(40) NOT NULL,
    FOREIGN KEY(id_grupo) REFERENCES grupos(id) ON DELETE CASCADE
);

/*Crea la tabla historial con los datos id_usuario, 
fecha_hora (la fecha y hora de la modificacion), tipo (el tipo de modificacion), tabla (la 
tabla de la modificacion), id_fila (el id de la fila modificada), 
datos_viejos (los datos antes de la modificacion) y datos_nuevos (los
datos nuevos). Todos los cambios a la base de datos por los usuarios
serán registrados en esta tabla*/
CREATE TABLE IF NOT EXISTS historial(
    id_usuario INTEGER NOT NULL,
    fecha_hora VARCHAR(30) NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    tabla VARCHAR(20) NOT NULL,
    id_fila VARCHAR(4),
    datos_viejos VARCHAR(400),
    datos_nuevos VARCHAR(400)
)