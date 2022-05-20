import sqlite3 as db
import os

#se crea la base de datos

con=db.Connection(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sqlite3")
cur=con.cursor()
with open(f"{os.path.abspath(os.getcwd())}/duraam/db/duraam.sql",'r', encoding='utf-8') as codigoSQL:
    codigoSQL=codigoSQL.read().split(';')
    for statement in codigoSQL:
        cur.execute(statement)
    con.commit()
