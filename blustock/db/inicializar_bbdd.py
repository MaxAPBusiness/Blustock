"""Este módulo crea la conexión a la base de datos.

Si la base de datos no estaba creada, la crea con todas sus tablas.
"""
import sqlite3 as db
import os

# Se conecta a la base de datos
con = db.Connection(
    f"{os.path.abspath(os.getcwd())}{os.sep}db{os.sep}blustock.sqlite3")
# Crea el cursor
cur = con.cursor()

# Abre el archivo blustock.sql
with open(f"{os.path.abspath(os.getcwd())}{os.sep}db{os.sep}blustock.sql", 'r', encoding='utf-8') as codigoSQL:
    # Con la función split, separa cada statement (es decir, cada código) en una lista.
    # Recorre la lista y ejecuta cada código.
    for statement in codigoSQL.read().split(';'):
        cur.execute(statement)
    # Guarda los cambios en la base de datos.
    con.commit()
