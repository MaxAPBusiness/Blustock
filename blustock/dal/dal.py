import os
from db.bdd import bdd

class DAL():
    def obtenerDatos(
        self, tabla: str, busqueda: str, 
        filtrosExtra: list | tuple | dict | None = None):
        with open(f"dal{os.sep}queries{os.sep}{tabla}.sql", 'r') as queryText:
            query=queryText.read()
            filtro = []
            if filtrosExtra:
                cantCamposFiltroExtra=len(filtrosExtra)
                filtro.extend(filtrosExtra)
            else:
                cantCamposFiltroExtra=0
            for i in range(query.count('?')-cantCamposFiltroExtra):
                filtro.append(f"%{busqueda}%")
            return bdd.cur.execute(query, filtro).fetchall()

dal=DAL()