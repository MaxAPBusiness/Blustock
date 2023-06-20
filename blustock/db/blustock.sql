CREATE TABLE IF NOT EXISTS "clases" (
	"id"	INTEGER NOT NULL UNIQUE,
	"descripcion"	VARCHAR(40) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "estados" (
	"id"	INTEGER NOT NULL UNIQUE,
	"descripcion"	VARCHAR(40) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "grupos" (
	"id"	INTEGER NOT NULL UNIQUE,
	"descripcion"	VARCHAR(40) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "historial" (
	"id_usuario"	INTEGER NOT NULL,
	"fecha_hora"	VARCHAR(30) NOT NULL,
	"tipo"	VARCHAR(30) NOT NULL,
	"tabla"	VARCHAR(20) NOT NULL,
	"id_fila"	INTEGER,
	"datos_viejos"	VARCHAR(400),
	"datos_nuevos"	VARCHAR(400),
	FOREIGN KEY("id_usuario") REFERENCES "personal"("id") ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS "movimientos" (
	"id"	INTEGER NOT NULL,
	"id_turno"	INTEGER,
	"id_elem"	INTEGER NOT NULL,
	"id_estado"	INTEGER NOT NULL,
	"cant"	INTEGER NOT NULL,
	"id_persona"	INTEGER NOT NULL,
	"fecha_hora"	VARCHAR(24) NOT NULL,
	"id_tipo"	INTEGER NOT NULL,
	"descripcion"	VARCHAR(400),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_persona") REFERENCES "personal"("id") ON UPDATE CASCADE,
	FOREIGN KEY("id_elem") REFERENCES "stock"("id") ON UPDATE CASCADE,
	FOREIGN KEY("id_turno") REFERENCES "turnos"("id") ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS "personal" (
	"id"	INTEGER NOT NULL UNIQUE,
	"nombre_apellido"	VARCHAR(50) NOT NULL,
	"dni"	INTEGER NOT NULL UNIQUE,
	"id_clase"	VARCHAR(40) NOT NULL,
	"usuario"	VARCHAR(20) UNIQUE,
	"contrasena"	VARCHAR(75),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "reparaciones" (
	"id"	INTEGER NOT NULL UNIQUE,
	"id_herramienta"	INTEGER NOT NULL,
	"cantidad"	INTEGER NOT NULL,
	"id_usuario"	INTEGER NOT NULL,
	"destino"	VARCHAR(50) NOT NULL,
	"fecha_envio"	VARCHAR(24) NOT NULL,
	"fecha_regreso"	VARCHAR(24),
	FOREIGN KEY("id") REFERENCES "personal"("id") ON UPDATE CASCADE,
	FOREIGN KEY("id_herramienta") REFERENCES "stock"("id") ON UPDATE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "stock" (
	"id"	INTEGER NOT NULL UNIQUE,
	"descripcion"	VARCHAR(100) NOT NULL,
	"cant_condiciones"	INTEGER NOT NULL,
	"cant_reparacion"	INTEGER,
	"cant_baja"	INTEGER,
	"id_subgrupo"	INTEGER NOT NULL,
	"id_ubi"	INTEGER NOT NULL,
	FOREIGN KEY("id_ubi") REFERENCES "ubicaciones"("id") ON DELETE CASCADE,
	FOREIGN KEY("id_subgrupo") REFERENCES "subgrupos"("id") ON DELETE CASCADE,
	CONSTRAINT "unique_stock" UNIQUE("descripcion","id_ubi"),
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "subgrupos" (
	"id"	INTEGER NOT NULL UNIQUE,
	"descripcion"	VARCHAR(40) NOT NULL,
	"id_grupo"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_grupo") REFERENCES "grupos"("id") ON DELETE CASCADE,
	UNIQUE("descripcion","id_grupo")
);

CREATE TABLE IF NOT EXISTS "tipos_mov" (
	"id"	INTEGER NOT NULL UNIQUE,
	"descripcion"	VARCHAR(40) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "turnos" (
	"id"	INTEGER NOT NULL UNIQUE,
	"id_panolero"	INTEGER NOT NULL,
	"fecha_ing"	VARCHAR(20) NOT NULL,
	"fecha_egr"	VARCHAR(12),
	"id_prof_ing"	INTEGER NOT NULL,
	"id_prof_egr"	INTEGER,
	"id_ubi"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_ubi") REFERENCES "ubicaciones"("id") ON UPDATE CASCADE,
	FOREIGN KEY("id_prof_egr") REFERENCES "personal"("id") ON UPDATE CASCADE,
	FOREIGN KEY("id_panolero") REFERENCES "personal"("id") ON UPDATE CASCADE,
	FOREIGN KEY("id_prof_ing") REFERENCES "personal"("id") ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS "ubicaciones" (
	"id"	INTEGER NOT NULL UNIQUE,
	"descripcion"	VARCHAR(40) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

