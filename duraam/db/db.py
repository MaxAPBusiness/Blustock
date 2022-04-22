import sqlite3 as db
import os



#se crea la base de datos

con=db.Connection(f"{os.path.abspath(os.getcwd())}/proyecto-panol/db.sqlite3")
cur=con.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS Alumnos(
DNI VARCHAR(8) PRIMARY KEY,
Nombre VARCHAR(40),
Apellido VARCHAR(40),
Usuario VARCHAR(16),
Contraseña VARCHAR(16),
Mail VARCHAR(40)
)""")
