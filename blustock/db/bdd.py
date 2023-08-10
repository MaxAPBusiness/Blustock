"""Este módulo crea la conexión a la base de datos.

Si la base de datos no estaba creada, la crea con todas sus tablas.

Clases
------
    BDD():
        Crea la base de datos y le ingresa datos por defecto.
"""
import sqlite3 as db
import os

class BDD():
    """Esta clase crea la base de datos y le ingresa datos por
    defecto.
    
    Métodos
    -------
        __init__(self):
            El constructor, inicializa la conexión y el cursor.

        refrescarBDD(self):
            Carga datos por defecto a la base de datos.
    """
    def __init__(self):
        """El constructor, inicializa la conexión y el cursor."""
        # Se conecta a la base de datos
        self.con = db.Connection(
            f"db{os.sep}blustock.sqlite3")
        # Crea el cursor
        self.cur = self.con.cursor()
        
    def refrescarBDD(self):
        """Este método carga datos por defecto a la base de datos."""
        # Abre el archivo blustock.sql
        with open(f"db{os.sep}blustock.sql", 'r', encoding='utf-8') as codigoSQL:
            # Con la función split, separa cada statement (es decir, cada código) en una lista.
            # Recorre la lista y ejecuta cada código.
            for statement in codigoSQL.read().split(';'):
                self.cur.execute(statement)
            # Guarda los cambios en la base de datos.
            self.con.commit()

bdd=BDD()