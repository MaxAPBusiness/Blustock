"""Este módulo crea la conexión a la base de datos.

Clases
------
    BDD():
        Crea la base de datos y su cursor correspondiente.
"""
import sqlite3 as db
import os

class BDD():
    """Esta clase crea la base de datos y su cursor correspondiente.
    
    Métodos
    -------
        __init__(self):
            El constructor, inicializa la conexión y el cursor.
    """
    def __init__(self):
        """El constructor, inicializa la conexión y el cursor."""
        # Se conecta a la base de datos
        self.con = db.Connection(
            f"db{os.sep}blustock.sqlite3")
        # Crea el cursor
        self.cur = self.con.cursor()

bdd = BDD()