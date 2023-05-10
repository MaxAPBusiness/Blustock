/*Este es el código SQL de la base de datos*/

/*Crea la tabla de personal con su dni (PK), nombre y apellido,
tipo, usuario y contraseña*/
CREATE TABLE IF NOT EXISTS personal(
    dni INTEGER PRIMARY KEY,
    nombre_apellido VARCHAR(50) NOT NULL,
    tipo VARCHAR(40) NOT NULL,
    usuario VARCHAR(20) UNIQUE,
    contrasena VARCHAR(75)
);

/*Crea la tabla de grupos con su id (PK) y su nombre*/
CREATE TABLE IF NOT EXISTS grupos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion VARCHAR(40) NOT NULL
);

/*Crea la tabla de subgrupos con su id (PK), su nombre y el grupo
al que pertenece(FK)*/
CREATE TABLE IF NOT EXISTS subgrupos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion VARCHAR(40) NOT NULL,
    id_grupo INTEGER NOT NULL,
    FOREIGN KEY(id_grupo) REFERENCES grupos(id) ON DELETE CASCADE
);

/*Crea la tabla de stock con el id (PK) de la herramienta o insumo,
descripción (nombre), cantidad en condiciones, cantidad en 
reparación, cantidad de baja (los insumos no tendrán ni cantidad
en reparación ni de baja) y el subgrupo al que pertenece (FK).*/
CREATE TABLE IF NOT EXISTS stock(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion VARCHAR(100) NOT NULL,
    cant_condiciones INTEGER NOT NULL,
    cant_reparacion INTEGER,
    cant_baja INTEGER,
    id_subgrupo INTEGER NOT NULL,
    FOREIGN KEY(id_subgrupo) REFERENCES subgrupos(id)
    ON DELETE CASCADE
);

/*Crea la tabla de turnos con su id (PK), fecha, id del panolero
(FK), hora de ingreso del pañolero, hora de egreso, id del 
profesor que autorizó el ingreso (FK) e id del profesor que 
autorizó el egreso (FK)*/
CREATE TABLE IF NOT EXISTS turnos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_panolero INTEGER,
    fecha VARCHAR(12),
    hora_ing VARCHAR(12) NOT NULL,
    hora_egr VARCHAR(12),
    prof_ing INTEGER NOT NULL,
    prof_egr INTEGER,
    FOREIGN KEY(id_panolero) REFERENCES personal(dni)
    ON DELETE CASCADE,
    FOREIGN KEY(prof_ing) REFERENCES personal(dni)
    ON DELETE CASCADE,
    FOREIGN KEY(prof_egr) REFERENCES personal(dni)
    ON DELETE CASCADE
);

/*Crea la tabla de movimientos con su id (PK), id del turno en el
que se hizo el movimiento (FK), id del elemento (herramienta o
insumo) (FK), estado del elemento, cantidad, id de la persona que 
hizo el movimiento (FK), fecha y hora, tipo de movimiento y una
descripción opcional en la que, si volvierpn rotas las 
herramientas, se explique por qué*/
CREATE TABLE IF NOT EXISTS movimientos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_turno INTEGER,
    id_elem INTEGER NOT NULL,
    estado INTEGER NOT NULL,
    cant INTEGER NOT NULL,
    id_persona INTEGER NOT NULL,
    fecha_hora VARCHAR(24) NOT NULL,
    tipo INTEGER NOT NULL,
    descripcion VARCHAR(100),
    FOREIGN KEY(id_turno) REFERENCES turnos(id) ON DELETE CASCADE,
    FOREIGN KEY(id_elem) REFERENCES stock(id) ON DELETE CASCADE,
    FOREIGN KEY(id_persona) REFERENCES personal(dni) ON DELETE CASCADE
);

/*Crea la tabla historial_de_cambios con los datos id_usuario,
rol (el rol del usuario), fecha_hora (la fecha y hora de la
modificacion), tipo (el tipo de modificacion), tabla (la 
tabla de la modificacion), id_fila (el id de la fila modificada), 
datos_viejos (los datos antes de la modificacion) y datos_nuevos (los
datos nuevos)*/
CREATE TABLE IF NOT EXISTS historial_de_cambios(
    id_usuario INTEGER,
    fecha_hora VARCHAR(30) NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    tabla VARCHAR(20) NOT NULL,
    id_fila VARCHAR(4),
    datos_viejos VARCHAR(400),
    datos_nuevos VARCHAR(400)
)